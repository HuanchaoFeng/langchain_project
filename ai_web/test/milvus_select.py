from pymilvus import MilvusClient
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD

client = MilvusClient(
    uri=MILVUS_URL,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD
)

print(f"collections:{client.list_collections()}")
print(f"indexes:{client.list_indexes("rag_test")}")

# 加载到内存
client.load_collection("rag_test")

res = client.query(
    collection_name="rag_test",
    filter="doc_id == 'text'",
    output_fields=["id", "doc_id", "chunk"]
)

print(f"查询结果：{res}")