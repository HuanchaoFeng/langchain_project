# Service 请求入口
from fastapi import FastAPI
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from workflow.application import chat_with_qwen

app = FastAPI()

@app.get("/chat")
def chat_api(user_input: str, session_id: str, username: str):
    return  chat_with_qwen(user_input, session_id, username)
