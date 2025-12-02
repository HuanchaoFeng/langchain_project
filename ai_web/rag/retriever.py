from milvus_util import milvus_search
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import QWEN_EMBEDDING_MODEL, QWEN_API_KEY
from langchain_community.embeddings import DashScopeEmbeddings


# 全局用一个
embedding_model = DashScopeEmbeddings(
        dashscope_api_key = QWEN_API_KEY,
        model = QWEN_EMBEDDING_MODEL
)


# 模型RAG入口
def retriever(query, collection_name):
    relas_contexts = milvus_search(query, embedding_model, collection_name)
    context_text = "\n".join(relas_contexts)
    return context_text


if __name__ == "__main__":
    print(retriever("测试相关信息", "rag_test"))