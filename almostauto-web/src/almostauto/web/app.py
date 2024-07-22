from almostauto.web.templates import templates_router
from litestar import get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.contrib.htmx.request import HTMXRequest
from litestar.static_files import create_static_files_router

from litestar import Litestar, get

from pathlib import Path


@get("/")
async def get_home() -> Template:
    return Template(template_name="pages/home.html.jinja2")


app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["assets"]),
        get_home,
        templates_router,
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
    request_class=HTMXRequest,
)
