from pydantic import BaseModel
from typing import Any, List, Optional

class Result(BaseModel):
    success: bool
    errorMsg: Optional[str] = None
    data: Optional[Any] = None
    total: Optional[int] = None

    @staticmethod
    def ok(data=None, total=None):
        return Result(success=True, errorMsg=None, data=data, total=total)

    @staticmethod
    def ok_list(data: List[Any], total: int):
        return Result(success=True, errorMsg=None, data=data, total=total)

    @staticmethod
    def fail(error_msg: str):
        return Result(success=False, errorMsg=error_msg)
