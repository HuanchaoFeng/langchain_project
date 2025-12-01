from langchain_community.embeddings import DashScopeEmbeddings
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import QWEN_API_KEY, QWEN_EMBEDDING_MODEL
from milvus_util import milvus_insert
# 嵌入模块：用于把document转变为嵌入向量、存入向量数据库

def get_embed_model():
    embedding_model = DashScopeEmbeddings(
        dashscope_api_key = QWEN_API_KEY,
        model = QWEN_EMBEDDING_MODEL
    )
    return embedding_model

# 对切分后的文档进行embedding操作
def get_emb(documents, collection_name):
    model = get_embed_model()
    milvus_datas = []
    for doc in documents:
        id = doc["doc_id"]
        chunk = doc["doc_chunk"]
        vector = model.embed_query(chunk)
        milvus_datas.append({
            "doc_id": id,
            "chunk": chunk,
            "vector": vector
        })
    result = milvus_insert(milvus_datas, collection_name)
    return result


if __name__ == "__main__":
    collection_name = "rag_test"
    # 输入样例就长这样，再process_doc模块切分文件的时候，必须变成下面这个样子
    documents = [{"doc_id":"text", "doc_chunk":"what's this 4?"}]
    print(get_emb(documents, collection_name))




    

