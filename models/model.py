from pydantic import BaseModel


class AnalyzeRequest(BaseModel):
    sentence: str
    cursor_index: int
