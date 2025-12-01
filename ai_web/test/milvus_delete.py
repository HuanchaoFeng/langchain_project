from pymilvus import MilvusClient
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD

# 根据doc_id删除文档

client = MilvusClient(
    uri=MILVUS_URL,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD
)

result = client.delete(
    collection_name="rag_test",
    filter="doc_id == 'text_1'"
)

print(f"删除结果：{result}")