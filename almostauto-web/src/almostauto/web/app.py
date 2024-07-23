from litestar import Request, get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.contrib.htmx.request import HTMXRequest
from litestar.static_files import create_static_files_router
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from litestar import Litestar, get

from pathlib import Path


@get("/")
async def get_home() -> Template:
    return Template(template_name="pages/home.html.jinja2")


def http_404(_: Request, exc: Exception) -> Template:
    return Template(template_name="pages/404.html.jinja2")


def http_500(_: Request, exc: Exception) -> Template:
    return Template(template_name="pages/500.html.jinja2")



app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["assets"]),
        get_home,
        templates_router,
    ],
    exception_handlers={
        HTTP_404_NOT_FOUND: http_404,
        HTTP_500_INTERNAL_SERVER_ERROR: http_500
        },
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    request_class=HTMXRequest,
)
