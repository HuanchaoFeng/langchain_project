import os
import getpass
from langchain_openai import ChatOpenAI
from langchain.messages import HumanMessage, SystemMessage, AIMessage

qwen_flash = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-d9b21546c7834606842410a43b284a03",
    model="qwen-flash"
)

system_message = SystemMessage("You are a weather assistant.")
user_message = HumanMessage("Can you tell me the shenzhen's weather today?")

message = [system_message, user_message]

answer = qwen_flash.invoke(message)

print(f"question:{system_message.content + user_message.content}\nanswer:{answer.content}")