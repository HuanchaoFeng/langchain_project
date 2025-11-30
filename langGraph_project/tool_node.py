# 定义模型
from langchain_openai import ChatOpenAI
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from config import QWEN_CHAT_MODEL_URL, API_KEY
model = ChatOpenAI(
    base_url=QWEN_CHAT_MODEL_URL,
    api_key=API_KEY,
    model="qwen-plus"
)

# 定义工具
from langchain.tools import tool

@tool
def multiply(a: int, b: int) -> int:
    """
    进行乘法运算.
    Args:
    a: int
    b: int
    """
    return a * b

@tool
def add(a: int, b: int) -> int:
    """
    进行加法运算
    Args:
    a: int
    b: int
    """
    return a + b

tools = [add, multiply]
model_with_tools = model.bind_tools(tools) # 绑定工具

# 定义state

from langchain.messages import AnyMessage
from typing_extensions import TypedDict, Annotated
import operator

# 在内置 MessagesState 的基础上增加了一个字段：llm_calls
class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], operator.add] # 追加
    llm_calls: int # 覆盖

# 定义结点
from langchain.messages import SystemMessage, ToolMessage
def llm_call(state: dict):

    return {
        "messages": [
            model_with_tools.invoke(
                [
                    SystemMessage(content="You are a helpful assistant tasked with performing arithmetic on a set of inputs.")
                ]
                + state["messages"]
            )
        ],
        "llm_calls": state.get('llm_calls', 0) + 1
    }

# 映射函数
tools_map = {
    tool.name: tool for tool in tools
}
def tool_node(state: dict):
    result = []
    tool_calls = state["messages"][-1].tool_calls
    for tool_call in tool_calls:
        observation = tools_map[tool_call["name"]].invoke(tool_call["args"])
        result.append(ToolMessage(content=observation, tool_call_id = tool_call["id"]))
    return {"messages": result}

# 条件函数
from typing import Literal
from langgraph.graph import StateGraph, START, END

def should_continue(state: dict) -> Literal["tool_node", "END"]:
    # 是否调用工具
    last_message = state["messages"][-1]
    if last_message.tool_calls:
        return "tool_node"
    return END

# 构建图
workflow = StateGraph(MessageState)
workflow.add_node("llm_call", llm_call)
workflow.add_node("tool_node", tool_node)
workflow.add_edge(START, "llm_call")
workflow.add_conditional_edges(
    "llm_call",
    should_continue,
    ["tool_node", END]
)
workflow.add_edge("tool_node", "llm_call") # 调用工具结果返回给llm、循环
react_agent = workflow.compile()

# 可视化
from IPython.display import Image, display
graph = react_agent.get_graph(xray=True)
data = graph.draw_mermaid_png()
with open("/home/data1/hcfeng/langchain_project/langGraph_project/tool_node.png", "wb") as f:
    f.write(data)


# 执行
from langchain.messages import HumanMessage
messages = [HumanMessage(content="you should give the answer: add 1 and 2.")]
messages = react_agent.invoke({"messages": messages})
for message in messages["messages"]:
    message.pretty_print()
