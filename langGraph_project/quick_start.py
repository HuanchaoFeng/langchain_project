from langgraph.graph import StateGraph, MessagesState, START, END
import sys
from langchain_openai import ChatOpenAI
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from config import API_KEY, QWEN_CHAT_MODEL_URL


def chat_with_model(state:MessagesState):
    qwen_model = ChatOpenAI(
        base_url = QWEN_CHAT_MODEL_URL,
        api_key = API_KEY,
        model = "qwen-plus"
    )
    return {"messages": [qwen_model.invoke(state["messages"][-1].content)]}

graph = StateGraph(MessagesState)
graph.add_node(chat_with_model)
graph.add_edge(START, "chat_with_model")
graph.add_edge("chat_with_model", END)
graph = graph.compile()
result = graph.invoke({"messages": [{"role": "user", "content": "Who are you ?"}]})
print(f"执行结果: {result}")