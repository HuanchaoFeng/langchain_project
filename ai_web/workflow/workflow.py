from langchain_openai import ChatOpenAI
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import QWEN_API_KEY, QWEN_CHAT_MODEL_URL, QWEN_CHAT_MODEL
from typing_extensions import TypedDict
from operator import add
from langchain.messages import AnyMessage
from typing import Annotated
from langgraph.graph import StateGraph, START, END
from system_template import RECOGNITION_PROMPT, CONTRACT_PROMPT, PAPER_PROMPT
from type_enum import TYPE_1, TYPE_2, TYPE_3

chat_model = ChatOpenAI(
    base_url = QWEN_CHAT_MODEL_URL,
    api_key = QWEN_API_KEY,
    model = QWEN_CHAT_MODEL
)

# 自定义流转的信息
class MessageState(TypedDict):
    messages: Annotated[list[AnyMessage], add]
    user_query: str
    intent: str

'''阿里云百炼example
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "你是谁？"}]
response = chatLLM.invoke(messages)
'''

# 定义节点，包括意图识别模型，分类：合同审查、文案审查、普通对话
def llm_recog(state: MessageState):
    system_message = [{"role": "system", "content": RECOGNITION_PROMPT}]
    user_query = state['messages'][-1]['content']
    human_message = [state['messages'][-1]]
    resp = chat_model.invoke(system_message + human_message)
    return {
        "user_query": user_query,
        "intent": resp.content.strip()
    }

def contract_check(state: MessageState):
    user_query = state["user_query"]
    system_message = [{"role": "system", "content": CONTRACT_PROMPT}]
    human_message = [{"role": "user", "content": user_query}]
    resp = chat_model.invoke(system_message + human_message)
    return {
        "messages": [
            {"role": "ai", "content": resp.content}
        ]
    }

def paper_check(state: MessageState):
    user_query = state["user_query"]
    system_message = [{"role": "system", "content": PAPER_PROMPT}]
    human_message = [{"role": "user", "content": user_query}]
    resp = chat_model.invoke(system_message + human_message)
    return {
        "messages": [
            {"role": "ai", "content": resp.content}
        ]
    }

def normal_llm(state: MessageState):
    user_query = state["user_query"]
    system_message = [{"role": "system", "content": CONTRACT_PROMPT}]
    human_message = [{"role": "user", "content": user_query}]
    resp = chat_model.invoke(system_message + human_message)
    return {
        "messages": [
            {"role": "ai", "content": resp.content}
        ]
    }

# 分类器
def classify_node(state:MessageState):
    intent = state["intent"].strip()
    if intent == TYPE_1:  
        return "contract_check"
    elif intent == TYPE_2:     
        return "paper_check"
    else:         
        return "normal_llm"

chat_flow = StateGraph(MessageState)
chat_flow.add_node("llm_recog", llm_recog)
chat_flow.add_node("paper_check", paper_check)
chat_flow.add_node("contract_check", contract_check)
chat_flow.add_node("normal_llm", normal_llm)
chat_flow.add_edge(START, "llm_recog")
chat_flow.add_edge("paper_check", END)
chat_flow.add_edge("contract_check", END)
chat_flow.add_edge("normal_llm", END)
chat_flow.add_conditional_edges(
    "llm_recog",
    classify_node,
    {
        "contract_check": "contract_check",
        "paper_check": "paper_check",
        "normal_llm": "normal_llm"
    }
)

app = chat_flow.compile()

if __name__ == "__main__":
    init_state: MessageState = {
        "messages": [
            {"role": "user", "content": "请润色这句话: 错过了落日余晖，还可以静待满天繁星"}
        ],
        "user_query": "",
        "intent": ""
    }
    result_state = app.invoke(init_state)

    print("最终状态：", result_state)
    print("对话历史：")
    for msg in result_state["messages"]:
        print(msg["role"], ":", msg["content"])

