from typing import Annotated
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.static_files import create_static_files_router

from litestar.params import Body
from litestar.enums import RequestEncodingType

from litestar import Litestar, get, delete, post

from litestar.status_codes import HTTP_200_OK

from pathlib import Path

from dataclasses import dataclass


from almostauto.db.tables import Templates


@dataclass
class AATemplate:
    id: int
    title: str


DATA = {
    1: AATemplate(1, "Test title")
}
DATA_NEXT_ID = 2


@get("/")
async def get_home(request: HTMXRequest) -> Template:
    return Template(template_name="pages/home.html.jinja2")


@get("/templates")
async def get_templates(request: HTMXRequest) -> Template:
    return Template(template_name="pages/templates.html.jinja2", context={"templates": DATA.values()})


@dataclass
class AATemplateSubmit:
    title: str


@post("/templates")
async def post_template(request: HTMXRequest, data: Annotated[AATemplateSubmit, Body(media_type=RequestEncodingType.URL_ENCODED)]) -> Template:
    global DATA_NEXT_ID
    DATA[DATA_NEXT_ID] = AATemplate(DATA_NEXT_ID, AATemplate(DATA_NEXT_ID, data.title))
    DATA_NEXT_ID += 1
    return Template(template_name="fragments/templates-view.html.jinja2")


@get("/templates/new")
async def get_templates_new(request: HTMXRequest) -> Template:
    return Template(template_name="pages/templates-new.html.jinja2")


@delete("/templates/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template(template_id: int) -> None:
    if template_id in DATA:
        del DATA[template_id]


@get("/templates/{template_id:int}")
async def get_template(request: HTMXRequest, template_id: int) -> Template:
    template = DATA[template_id]
    return Template(template_name="pages/templates-id.html.jinja2", context={"template": template})


@get("templates/{template_id:int}/edit")
async def get_template_id_edit(request: HTMXRequest, template_id: int) -> Template:
    template = DATA[template_id]
    return Template(template_name="fragments/templates-edit.html.jinja2", context={"template": template})


app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["assets"]),
        get_home,
        get_templates,
        post_template,
        get_templates_new,
        get_template,
        delete_template,
        get_template_id_edit
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
