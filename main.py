from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from mikann import analyze_text,_cursor_word
app = FastAPI()


class SentenceRequest(BaseModel):
    sentence: str
    cursor_index: str


@app.post("/")
async def root(request: SentenceRequest):
    try:
        # 处理输入的句子
        print(request.sentence)
        return {"message": "Hello World"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
async def analyze(sentence: str = Query(..., description="Input sentence"),
                  cursor_index: int = Query(..., description="Cursor index")):
    try:
        # 处理输入的句子
        print(f"Sentence: {sentence}, Cursor Index: {cursor_index}")
        result = analyze_text("晩ご飯を食べましたか。")
        return _cursor_word(result, cursor_index)
        # return {"message": "Processing successful", "sentence": sentence, "cursor_index": cursor_index}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
