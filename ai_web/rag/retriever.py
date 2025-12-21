from milvus_util import milvus_search
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import QWEN_EMBEDDING_MODEL, QWEN_API_KEY, QWEN_RERANKER_MODEL
from langchain_community.embeddings import DashScopeEmbeddings
from rag.reranker_util import DashScopeReranker

# 全局用一个
embedding_model = DashScopeEmbeddings(
        dashscope_api_key = QWEN_API_KEY,
        model = QWEN_EMBEDDING_MODEL
)

# 重排序模型
reranker = DashScopeReranker(QWEN_RERANKER_MODEL, top_n=2)

# 模型RAG入口
def retriever(query, collection_name):
    relas_contexts = milvus_search(query, embedding_model, collection_name)
    reranker_result = reranker.rerank(query, relas_contexts)
    context_text = "\n".join(item["text"] for item in reranker_result)
    return context_text


if __name__ == "__main__":
    print(retriever("测试相关信息", "rag_test"))