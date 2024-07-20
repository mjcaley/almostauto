from almostauto.web.templates import TemplatesController
from litestar import get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
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
        TemplatesController,
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
