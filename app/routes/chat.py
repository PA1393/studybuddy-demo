from fastapi import APIRouter

from app.chat import suggest_partners
from app.matching import rank_partners
from app.signup import USERS

router = APIRouter()


@router.post("/chat")
def chat(user_email: str, message: str):
    user = next(u for u in USERS if u["email"] == user_email)
    candidates = rank_partners(user, [u for u in USERS if u is not user])
    return {"reply": suggest_partners(user, message, candidates[:5])}
