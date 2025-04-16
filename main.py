from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from mikann import analyze_text, _cursor_word

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class SentenceRequest(BaseModel):
    sentence: str
    cursor_index: str


class AnalyzeRequest(BaseModel):
    sentence: str
    cursor_index: int


@app.post("/")
def post_analyze(request: AnalyzeRequest):
    try:
        sentence = request.sentence
        cursor_index = request.cursor_index
        # 处理输入的句子
        print(f"Sentence: {sentence}, Cursor Index: {cursor_index}")
        result = analyze_text(sentence)
        cursor_jishokei = _cursor_word(result, cursor_index)
        print(cursor_jishokei)
        return {"jishokei": f"{cursor_jishokei}"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def get_analyze(
    sentence: str = Query(..., description="Input sentence"),
    cursor_index: int = Query(..., description="Cursor index"),
):
    """

    Args:
        sentence: 完整的上下文。
        cursor_index: 光标在句子中的位置。

    Returns:

    """
    try:
        print(f"Sentence: {sentence}, Cursor Index: {cursor_index}")
        result = analyze_text(sentence)
        cursor_jishokei = _cursor_word(result, cursor_index)
        print(cursor_jishokei)
        return {"jishokei": f"{cursor_jishokei}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
