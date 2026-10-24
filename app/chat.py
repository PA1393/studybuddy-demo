from openai import OpenAI

client = OpenAI()


def suggest_partners(user: dict, message: str, candidates: list[dict]) -> str:
    """Ask the AI to suggest study partners for this user."""
    candidate_text = "\n".join(f"{c['name']} <{c['email']}>" for c in candidates)
    prompt = (
        f"User {user['name']} ({user['email']}) says: {message}\n"
        f"Possible partners:\n{candidate_text}\n"
        "Suggest the best study partners."
    )
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content
