from pymilvus import MilvusClient
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD, QWEN_API_KEY, QWEN_EMBEDDING_MODEL
from langchain_community.embeddings import DashScopeEmbeddings

embeddding_model = DashScopeEmbeddings(
    dashscope_api_key=QWEN_API_KEY,
    model=QWEN_EMBEDDING_MODEL
)

query = "What's this?"
query_vector = embeddding_model.embed_query(query)

print(f"向量维度：{len(query_vector)}")

database = MilvusClient(
    uri=MILVUS_URL,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD
)

rows = []
rows.append({"chunk": query, "vector": query_vector, "doc_id": "text_1"})

result = database.insert(
    collection_name="rag_test",
    data=rows
)

print(f"插入结果:{result}")
