# rag/api.py
from fastapi import APIRouter, UploadFile, BackgroundTasks
from uuid import uuid4
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))
from dto.result import Result

from rag.embedding import execute_embedding

rag_router = APIRouter()

UPLOAD_DIR = Path("D:\\VscodeProject\\langchain_project\\ai_web\\rag\\konwledge")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

collection_name = "rag_test"


@rag_router.post("/upload")
async def upload_file(file: UploadFile, background_tasks: BackgroundTasks):
    
    doc_id = str(uuid4())
    if not file:
        return Result.fail("未检测到上传文件")

    if not file.filename:
        return Result.fail("文件名为空")

    stem = Path(file.filename).stem
    suffix = Path(file.filename).suffix
    save_path = UPLOAD_DIR / f"{stem}__{doc_id}{suffix}"

    with open(save_path, "wb") as f:
        f.write(await file.read())

    # 注册后台任务
    background_tasks.add_task(
        execute_embedding,
        file_path=str(save_path),
        collection_name="rag_test"
    )

    # TODO :得再加一个数据库存储文件任务，用于记录当前任务状态，用于给前端访问状态，并且记录嵌入操作是否成功

    return Result.ok(data="上传文件成功，正在进行嵌入操作")
