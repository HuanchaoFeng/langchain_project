from langchain.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai import ChatOpenAI

qwen_flash = ChatOpenAI(
    base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key="sk-d9b21546c7834606842410a43b284a03",
    model = "qwen-flash"
)

message1 = [SystemMessage("You are a weather assistant."), HumanMessage("Can you tell me the shenzhen's weather today?")]
messgae2 = [SystemMessage("You are a weather assistant."), HumanMessage("Can you tell me the guangzhou's weather today?")]

responses = qwen_flash.batch([message1, messgae2])

count = 0
for resp in responses:
    print(f"index:{count}:\nresp.content:{resp.content}")
    count += 1