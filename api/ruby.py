from urllib.parse import unquote

from fastapi import APIRouter
from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from utils.make_ruby import add_furigana

router_ruby = APIRouter(prefix="/ruby", tags=["API", "Ruby"])

templates = Jinja2Templates(directory="templates/")


@router_ruby.get(
    "/{sentence}",
    response_class=HTMLResponse,
    summary="Handles furigana requests",
)
def ruby(request: Request, sentence: str):
    """
    Handles furigana requests.
        处理注音请求

    Args:
        request: The request object.
            请求对象
        sentence: The sentence to be annotated with furigana.
            需要标注读音的句子

    Returns:
        An HTML response containing the sentence with furigana annotations.
            以 HTML 格式返回已经标注读音的句子。
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
