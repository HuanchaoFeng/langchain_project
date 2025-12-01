from pymilvus import MilvusClient, DataType
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD


client = MilvusClient(
    uri = MILVUS_URL,
    user = MILVUS_USER,
    password = MILVUS_PASSWORD
)

schema = MilvusClient.create_schema(
    auto_id = True,
    enable_dynamic_field=True
)

schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
schema.add_field(field_name="chunk", datatype=DataType.VARCHAR, max_length=65535)
schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
schema.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=100)

collection_name = "rag_test"

collections = client.list_collections()
if collection_name in collections:
    client.drop_collection(collection_name)


client.create_collection(
    collection_name = collection_name,
    schema = schema
)

print(f"创建表rag_test成功")

# 创建索引

index_params = client.prepare_index_params()

index_params.add_index(
    field_name="id",
    index_type="AUTOINDEX"
)

index_params.add_index(
    field_name="vector", 
    index_type="AUTOINDEX",
    metric_type="COSINE"
)

client.create_index(
    collection_name=collection_name,
    index_params=index_params
)



