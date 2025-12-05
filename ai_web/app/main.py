from fastapi import FastAPI
from controller.chat_controller import chat_router

app = FastAPI()

# 注册路由
app.include_router(chat_router)
