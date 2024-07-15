from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.static_files import create_static_files_router

from litestar import Litestar, get, delete, post

from litestar.status_codes import HTTP_200_OK

from pathlib import Path


from dataclasses import dataclass


@dataclass
class AATemplate:
    id: int
    title: str


DATA = {
    1: AATemplate(1, "Test title")
}
DATA_NEXT_ID = 2


@get("/")
async def home(request: HTMXRequest) -> Template:
    return Template(template_name="home.html.jinja2")


@get("/templates")
async def templates(request: HTMXRequest) -> Template:
    return Template(template_name="templates.html.jinja2", context={"templates": DATA.values()})


@post("/templates")
async def create_template(request: HTMXRequest) -> Template:
    return Template()


@get("/templates/new")
async def templates_new(request: HTMXRequest) -> Template:
    return Template(template_name="templates-new.html.jinja2")


@delete("/templates/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template(template_id: int) -> None:
    if template_id in DATA:
        del DATA[template_id]


app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["assets"]),
        home,
        templates,
        create_template,
        templates_new,
        delete_template
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
