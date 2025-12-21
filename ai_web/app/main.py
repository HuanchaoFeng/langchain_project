from fastapi import FastAPI
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from controller.chat_controller import chat_router
from controller.rag_controller import rag_router
app = FastAPI()

# 注册路由
app.include_router(chat_router)
app.include_router(rag_router)
