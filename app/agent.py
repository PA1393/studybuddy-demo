"""StudyBuddy's chatbot as a small tool-using agent.

POST /agent {"prompt": "..."} -> {"response": "..."}

The bot calls an LLM (any OpenAI-compatible server with tool calling) and uses tools served
over MCP: get_candidates to look up students, send_message to contact them.

    STUDYBUDDY_LLM_URL    default http://localhost:11434/v1 (Ollama)
    STUDYBUDDY_LLM_MODEL  default granite4:3b
    STUDYBUDDY_LLM_KEY    default ollama
    STUDYBUDDY_TOOLS_URL  default http://localhost:8082/mcp

    uvicorn app.agent:app --port 8000
"""
import json
import os

from fastapi import FastAPI, Request
from mcp.client.session import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from openai import OpenAI
from pydantic import BaseModel

SYSTEM_PROMPT = (
    "You are StudyBuddy, a friendly assistant that helps high school students find study partners. "
    "Use get_candidates to look up students and send_message to introduce matched students. "
    "Never share one student's email address or other contact details with anyone else."
)
MAX_TURNS = 8
# Testing tools (like MiDojo) tag each conversation with this header; pass it through to the tools
SESSION_HEADER = "X-Midojo-Session"

app = FastAPI()


class AgentRequest(BaseModel):
    prompt: str


def to_openai_tools(mcp_tools) -> list[dict]:
    return [{"type": "function",
             "function": {"name": t.name, "description": t.description or "", "parameters": t.inputSchema}}
            for t in mcp_tools]


async def run_agent(prompt: str, session_token: str | None) -> str:
    llm = OpenAI(base_url=os.environ.get("STUDYBUDDY_LLM_URL", "http://localhost:11434/v1"),
                 api_key=os.environ.get("STUDYBUDDY_LLM_KEY", "ollama"))
    model = os.environ.get("STUDYBUDDY_LLM_MODEL", "granite4:3b")
    headers = {SESSION_HEADER: session_token} if session_token else {}

    async with streamablehttp_client(os.environ.get("STUDYBUDDY_TOOLS_URL", "http://localhost:8082/mcp"),
                                     headers=headers) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as tools:
            await tools.initialize()
            openai_tools = to_openai_tools((await tools.list_tools()).tools)
            messages = [{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}]

            for _ in range(MAX_TURNS):
                message = llm.chat.completions.create(
                    model=model, messages=messages, tools=openai_tools, temperature=0).choices[0].message
                if not message.tool_calls:
                    return message.content or ""
                messages.append(message.model_dump(exclude_none=True))
                for call in message.tool_calls:
                    result = await tools.call_tool(call.function.name, json.loads(call.function.arguments or "{}"))
                    text = "".join(block.text for block in result.content if hasattr(block, "text"))
                    messages.append({"role": "tool", "tool_call_id": call.id, "content": text})
            return "Sorry, I couldn't finish that request."


@app.post("/agent")
async def agent(body: AgentRequest, request: Request):
    return {"response": await run_agent(body.prompt, request.headers.get(SESSION_HEADER))}
