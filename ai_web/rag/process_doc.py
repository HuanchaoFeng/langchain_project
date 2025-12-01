import os
import pdfplumber
import markdown
from bs4 import BeautifulSoup
from langchain_text_splitters import RecursiveCharacterTextSplitter
from embedding import transfer_and_insert_emb
# pdf
def load_pdf(file_path):
    text = ""
    with pdfplumber.open(file_path) as f:
        for page in f.pages:
            text = text + page.extract_text() + "\n"
    return text

# markdown
'''
如果不转换为html: #, *, - 等符号会影响 embedding
'''
def load_markdown(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        md_text = f.read()

    html = markdown.markdown(md_text)
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text("\n")

# txt文件
def load_txt(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

# chunk分割
def split_chunk(text, chunk_size = 500, chunk_overlap = 50):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = chunk_size,
        chunk_overlap = chunk_overlap
    )
    return splitter.split_text(text)

def load_document(file_path):
    extend = os.path.splitext(file_path)[1].lower()

    if extend == ".pdf":
        return load_pdf(file_path)
    elif extend == ".md":
        return load_markdown(file_path)
    elif extend == ".txt":
        return load_txt(file_path)
    else:
        raise ValueError(f"暂时不支持{extend}格式的文件")


def file_to_documents(file_path):
    # 读取、切割、组装
    doc_id = os.path.basename(file_path)
    full_text = load_document(file_path)
    chunks = split_chunk(full_text)
    # 组装格式(embedding所需的格式，因为我先写了embedding才写这个文档程序)
    documents = []
    for chunk in chunks:
        documents.append({
            "doc_id": doc_id,
            "doc_chunk": chunk
        })
    return documents

if __name__ == "__main__":
    file_path = "D:\\VscodeProject\\langchain_project\\ai_web\\rag\\konwledge\\test.txt"
    collection_name = "rag_test"
    documents = file_to_documents(file_path)
    res = transfer_and_insert_emb(documents, collection_name)
    print(res)