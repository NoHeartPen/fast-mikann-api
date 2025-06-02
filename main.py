import os

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from api.examle import router_example
from api.ruby import router_ruby
from mikann import analyze_text, get_cursor_result

app = FastAPI(
    title="Mikann API",
    description="Morphological analyser based on Sudachi, designed for the retrieval of Japanese dictionaries.",
    version="0.0.1",
    debug=True,
)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_example)
app.include_router(router_ruby)


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


@app.get(
    "/",
    response_class=HTMLResponse,
)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
    )
