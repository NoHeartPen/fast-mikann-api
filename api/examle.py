from fastapi import APIRouter

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

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
