from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from mikann import scan_kannyouku

router_example = APIRouter(prefix="/example", tags=["Example"])

templates = Jinja2Templates(directory="templates/example")


@router_example.get(
    "/",
    response_class=HTMLResponse,
    summary="Example routes",
)
def example(request: Request):
    return templates.TemplateResponse(
        "example.html",
        {
            "request": request,
            "example_routes": [
                {"path": "/example/ruby", "description": "Example for making ruby"},
                {
                    "path": "/example/jishokei",
                    "description": "Example for getting cursor jishokei",
                },
                {
                    "path": "/example/kannyouku",
                    "description": "Example for kannyouku",
                },
            ],
        },
    )


@router_example.get(
    "/ruby",
    response_class=HTMLResponse,
    summary="Example for make ruby",
)
def ruby(request: Request):
    return templates.TemplateResponse(
        "ruby.html",
        {"request": request},
    )


@router_example.get(
    "/jishokei",
    response_class=HTMLResponse,
    summary="Example for get cursor jishokei",
)
def jishokei(request: Request):
    return templates.TemplateResponse(
        "jishokei.html",
        {"request": request},
    )


@router_example.get(
    "/kannyouku",
    response_class=HTMLResponse,
    summary="Example for get kannyouku",
)
def jishokei(request: Request):
    return templates.TemplateResponse(
        "kannyouku.html",
        {"request": request},
    )


from pydantic import BaseModel
from fastapi import HTTPException


class ScanKannyoukuRequest(BaseModel):
    text: str


@router_example.post(
    "/api/scan-kannyoku",
    summary="Scan text and return possible 慣用句 (via scan_kannyouku)",
)
def api_scan_kannyoku(payload: ScanKannyoukuRequest):
    try:
        phrases_raw = scan_kannyouku(payload.text)
        # 将 [("嘘を付く",)] / [{...}] 等统一整理为字符串列表
        phrases: list[str] = []
        if phrases_raw:
            for item in phrases_raw:
                # 期望是单元素元组 (midashi_index,)
                if isinstance(item, (list, tuple)):
                    if len(item) >= 1:
                        phrases.append(str(item[0]))
                elif isinstance(item, set):
                    # 集合不保序，尽量取出一个
                    for v in item:
                        phrases.append(str(v))
                        break
                else:
                    phrases.append(str(item))
        return {"phrases": phrases}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
