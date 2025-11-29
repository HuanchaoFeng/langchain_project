from openai import OpenAI
from config import API_KEY

client = OpenAI(
    api_key = API_KEY,
    base_url = "https://dashscope.aliyuncs.com/compatible-mode/v1"
)

with open("/home/data1/hcfeng/langchain_project/files/text_emb_test.txt", "r", encoding="utf-8") as file:
    embedding = client.embeddings.create(
        model = "text-embedding-v4",
        input = file,
        dimensions = 1024,
        encoding_format = "float"
    )

print(embedding.model_dump_json())



