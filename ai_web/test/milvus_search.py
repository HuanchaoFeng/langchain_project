from pymilvus import MilvusClient
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD, QWEN_API_KEY, QWEN_EMBEDDING_MODEL
from langchain_community.embeddings import DashScopeEmbeddings

client = MilvusClient(
    uri=MILVUS_URL,
    user=MILVUS_USER,
    password=MILVUS_PASSWORD
)

embeddding_model = DashScopeEmbeddings(
    dashscope_api_key=QWEN_API_KEY,
    model=QWEN_EMBEDDING_MODEL
)

query = "What's this?"
query_vector = embeddding_model.embed_query(query)

# limit：top k
res = client.search(
    collection_name="rag_test",
    data=[query_vector],
    limit=3, 
    output_fields=["chunk"]
)

for hits in res:
    print("TopK results:")
    for hit in hits:
        print(hit['entity']['chunk'])