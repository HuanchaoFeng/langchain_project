from pymilvus import MilvusClient, DataType
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import MILVUS_URL, MILVUS_USER, MILVUS_PASSWORD

# milvus util工具包
client = MilvusClient(
    uri = MILVUS_URL,
    user = MILVUS_USER,
    password = MILVUS_PASSWORD
)

# 创建表
def milvus_create(collection_name):
    
    schema = MilvusClient.create_schema(
        auto_id = True,
        enable_dynamic_field=True
    )

    schema.add_field(field_name="id", datatype=DataType.INT64, is_primary=True)
    schema.add_field(field_name="chunk", datatype=DataType.VARCHAR, max_length=65535)
    schema.add_field(field_name="vector", datatype=DataType.FLOAT_VECTOR, dim=1024)
    schema.add_field(field_name="doc_id", datatype=DataType.VARCHAR, max_length=100)

    collections = client.list_collections()
    if collection_name in collections:
        return "已存在该数据表"

    result = client.create_collection(
        collection_name = collection_name,
        schema = schema
    )

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

    return f"成功创建数据表:{result}"

# 根据文档id删除对应文档数据
def milvus_delete(doc_id):
    result = client.delete(
        collection_name="rag_test",
        filter=f"doc_id == '{doc_id}'"
    )
    return result

# 插入数据
def milvus_insert(datas, collection_name):
    result = client.insert(
        collection_name = collection_name,
        data = datas
    )
    return result

# RAG查询top k数据
def milvus_search(query, embedding_model, collection_name):

    query_vector = embedding_model.embed_query(query)
    # limit：top k
    res = client.search(
        collection_name=collection_name,
        data=[query_vector],
        limit=3, 
        output_fields=["chunk"]
    )

    final_result = []
    for hits in res:
        for hit in hits:
            final_result.append(hit['entity']['chunk'])

    return final_result

# 普通字段查询
def select_common(doc_id, collection_name):
    
    res = client.query(
        collection_name=collection_name,
        filter=f"doc_id == '{doc_id}'",
        output_fields=["id", "doc_id", "chunk"]
    )

    return res

if __name__ == "__main__":
    # 测试函数

    # 插入数据
    # query_vector = [0.3580376395471989]*1024
    # datas = [{"doc_id":"text", "chunk":"what's this?", "vector":query_vector}]
    # collection_name = "rag_test"
    # milvus_insert(datas, collection_name)

    # 普通查询
    doc_id = "text"
    collection_name = "rag_test"
    print(f"查询结果：{select_common(doc_id, collection_name)}")