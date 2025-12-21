from langchain_community.document_compressors.dashscope_rerank import DashScopeRerank
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from settings.local import QWEN_API_KEY, QWEN_RERANKER_MODEL

class DashScopeReranker:

    def __init__(self, model: str = "qwen3-rerank", top_n: int = None):
        self.top_n = top_n
        self.reranker = DashScopeRerank(
            model=model,
            top_n=top_n,
            dashscope_api_key=QWEN_API_KEY
        )

    def rerank(self, query: str, docs: list[str]):
        if not docs:
            return []

        results = self.reranker.rerank(
            documents=docs,
            query=query,
        )

        reranked = []
        for item in results:
            idx = item["index"]
            score = item["relevance_score"]
            reranked.append({
                "text": docs[idx],
                "score": score,
            })

        return reranked

if __name__ == "__main__":
    model_name = QWEN_RERANKER_MODEL
    top_n = 2
    reranker = DashScopeReranker(model_name, top_n)
    query = "文本3"
    docs = ["text1", "text2", "text3"]
    result = reranker.rerank(query, docs)
    print(result)
