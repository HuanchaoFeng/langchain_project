from langchain_openai.embeddings import OpenAIEmbeddings
from config import API_KEY


embedding_model = OpenAIEmbeddings(
    api_key = API_KEY,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1",
    model = "text-embedding-v4"
)

# 阿里云不兼容
query_emb = embedding_model.embed_query("what's this?")

doc_emb = embedding_model.embed_documents(["Hello, world!", "Goodbye, world!"])

print(f"query_emb:{query_emb}")
print(f"doc_emb:{doc_emb}")