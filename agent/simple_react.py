import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from langchain.tools import tool
from langchain_openai import ChatOpenAI
from langchain.agents import create_agent
from langchain.messages import HumanMessage, SystemMessage, AIMessage, ToolMessage
from config import API_KEY
@tool
def get_weather(location:str) -> str:
    """必须使用本工具来查询指定地点当前天气情况。输入为城市名称，返回天气描述。"""
    return f"It's sunny in {location}."

# 写个终结工具进行任务终结
@tool
def do_end() -> str:
    """调用本工具结束任务"""
    return "Ending"

model = ChatOpenAI(
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    api_key = API_KEY,
    model = "qwen-plus"
)

tools = [get_weather, do_end]

tools_map = {
    "get_weather": get_weather,
    "do_end": do_end
}

system_prompt=SystemMessage(
    "You are a weather assistant. "
    "When asked about the weather of any city, ALWAYS use the `get_weather` tool."
)
user_messgae = HumanMessage("Can you tell me the shenzhen's weather today?")

model_with_tools = model.bind_tools(tools)
messages = [
        SystemMessage(
            "You are a weather assistant. "
            "When asked about weather, ALWAYS use get_weather tool. "
            "When you finish answering, CALL `do_end` tool."
        ),
]
user_messgae = "Can you tell me the guangzhou's weather today?"
# messages.append({"role": "user", "content": user_messgae})
messages.append(HumanMessage(user_messgae))
resp = model_with_tools.invoke(messages)

step = 0
max_step = 3
agent_state = "Running"

# ReAct
while step < max_step and agent_state == "Running":
    if resp.tool_calls:
        tool_call = resp.tool_calls[0]
        tool_name = tool_call["name"]
        args = tool_call["args"]

        print(f"调用工具:{tool_name},参数:{args}")

        result = tools_map[tool_name].invoke(args)
        print(f"调用结果：{result}")

        messages.append(resp)
        messages.append(ToolMessage(
            content=result, 
            tool_call_id=tool_call["id"]
        ))
        if tool_name == "do_end":
            print("ReAct流程结束")
            agent_state = "Finished"
        resp = model_with_tools.invoke(messages)
        step = step + 1
    else:
        # 无工具调用，输出答案结束
        print(resp.content)
        agent_state = "Finished"

print(f"本次对话结果：{messages}")





