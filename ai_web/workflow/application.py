import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from workflow import app
from database.message_pool import chat_message

message_db = chat_message()
limit_session = 3

# 数据封装
def convert_history_to_messages(history_db):
    messages = []
    for row in history_db:
        role = row[2]
        content = row[3]
        if role == "user":
            messages.append({"role": "user", "content": content})
        elif role == "ai":
            messages.append({"role": "ai", "content": content})
    return messages

# 请求对话入口
def chat_with_qwen(query, session_id, username):
    # 查询历史记录<limit_session轮
    historys_db = message_db.get_session_message(session_id, limit_session * 2)
    historys_msg = convert_history_to_messages(historys_db)
    state = {
        "messages": historys_msg,
        "query": "",
        "intent": ""
    }
    # 添加当前轮次的query
    state["messages"].append({"role": "user", "content": query})
    resp = app.invoke(state)
    # 保存消息
    message_db.insert_message(query, resp["messages"][-1]["content"], session_id, username)

if __name__ == "__main__":
    query = "请润色这句话: 错过了落日余晖，还可以静待满天繁星"
    session_id = "session_id"
    username = "zhangsan"
    chat_with_qwen(query, session_id, username)