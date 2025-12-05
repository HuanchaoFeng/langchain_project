from fastapi import APIRouter
from workflow.application import chat_with_qwen

chat_router = APIRouter()

@chat_router.get("/chat")
def chat_api(user_input: str, session_id: str, username: str):
    return chat_with_qwen(user_input, session_id, username)
