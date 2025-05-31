import os
from urllib.parse import unquote

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from mikann import analyze_text, get_cursor_result
from utils.make_ruby import add_furigana

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
    "/ruby/{sentence}",
    response_class=HTMLResponse,
    tags=[
        "API",
    ],
    summary="处理注音请求",
)
def api_ruby(request: Request, sentence: str):
    """
    处理注音请求

    Args:
        request: 请求对象
        sentence: 需要标注读音的句子

    Returns:
        以HTML格式返回已经标注读音的句子。
    """
    # 解码 URL 编码
    decoded_sentence = unquote(sentence)
    added_ruby_text = add_furigana(decoded_sentence)
    return templates.TemplateResponse(
        request,
        "ruby.html",
        {
            "added_ruby_text": added_ruby_text,
        },
    )


@app.get(
    "/example",
    response_class=HTMLResponse,
    tags=[
        "Example",
    ],
    summary="测试页面",
)
def example(request: Request):
    return templates.TemplateResponse(
        request,
        "example.html",
    )


@app.get(
    "/example/ruby",
    response_class=HTMLResponse,
    tags=[
        "Example",
    ],
    summary="Example for make ruby",
)
def example(request: Request):
    return templates.TemplateResponse(
        "example/ruby.html",
        {"request": request},
    )


@app.get(
    "/example/jishokei",
    response_class=HTMLResponse,
    tags=[
        "Example",
    ],
    summary="Example for get cursor jishokei",
)
def jishokei_example(request: Request):
    return templates.TemplateResponse(
        "example/jishokei.html",
        {"request": request},
    )


@app.get(
    "/",
    response_class=HTMLResponse,
)
def index(request: Request):
    return templates.TemplateResponse(
        request,
        "index.html",
    )
