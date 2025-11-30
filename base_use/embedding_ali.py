from langchain_community.embeddings import DashScopeEmbeddings
from config import API_KEY, QWEN_EMBEDDING_MODEL

embedding_model = DashScopeEmbeddings(
    model = QWEN_EMBEDDING_MODEL,
    dashscope_api_key = API_KEY
)

text = "This is a test document."
query_result = embedding_model.embed_query(text)

doc_result = embedding_model.embed_documents(
    [
        "Hi there!",
        "Oh, hello!",
        "What's your name?"
    ]
)

print(f"query_result: {len(query_result)}")
print(f"doc_result: {len(doc_result[0])}")