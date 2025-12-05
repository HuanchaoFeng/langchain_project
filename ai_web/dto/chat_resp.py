from  pydantic import BaseModel
class ChatResp(BaseModel):
    role: str
    content: str
