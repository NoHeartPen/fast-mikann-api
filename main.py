from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from starlette.responses import RedirectResponse

from mikann import analyze_text, get_cursor_result

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
        result = analyze_text(sentence)
        cursor_jishokei = get_cursor_result(result, cursor_index)
        return {"jishokei": f"{cursor_jishokei}"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/")
def index():
    redict_url = "https://github.com/NoHeartPen/fast-mikann-api"
    return RedirectResponse(url=redict_url)
