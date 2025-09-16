import os

from fastapi import FastAPI, HTTPException, Request
from fastapi import status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException

from api.examle import router_example
from api.ruby import router_ruby
from mikann import analyze_text, get_cursor_result
from models.model import AnalyzeRequest

app = FastAPI(
    title="Mikann API",
    description="Morphological analyser based on Sudachi, designed for the retrieval of Japanese dictionaries.",
    version="0.0.1",
    debug=True,
)

templates = Jinja2Templates(
    directory=os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
)

app.mount(
    "/static",
    StaticFiles(directory=os.path.join(os.path.dirname(__file__), "static")),
    name="static",
)


@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """自定义 HTTP 异常 (如 404、403 等)"""
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": exc.status_code,
            "status_message": exc.detail if exc.detail else "Error",
            "error_message": "Oops! Something went wrong.",
        },
        status_code=exc.status_code,
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """自定义验证失败异常 (如请求参数错误)"""
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY,
            "status_message": "Validation Error",
            "error_message": str(exc),
        },
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """处理所有未捕获的异常"""
    return templates.TemplateResponse(
        "error.html",
        {
            "request": request,
            "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            "status_message": "Internal Server Error",
            "error_message": "An unexpected error occurred. Please try again later.",
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    )


@app.get("/cause_error")
async def cause_error():
    """手动触发一个示例异常以测试自定义错误页面"""
    raise HTTPException(status_code=404, detail="This is a custom 404 error.")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_example)
app.include_router(router_ruby)


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
