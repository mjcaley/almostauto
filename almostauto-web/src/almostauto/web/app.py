from typing import Annotated
from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get, Litestar
from litestar.response import Template

from litestar.contrib.jinja import JinjaTemplateEngine
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.static_files import create_static_files_router

from litestar.params import Body, Parameter

from litestar import Litestar, get, delete, post, put

from litestar.status_codes import HTTP_200_OK

from pathlib import Path

from almostauto.db import tables
from .models import EditTemplate, EditTemplateDTO, NewTemplate, NewTemplateDTO, ViewTemplate


@get("/")
async def get_home(request: HTMXRequest) -> Template:
    return Template(template_name="pages/home.html.jinja2")


@get("/templates")
async def get_templates(request: HTMXRequest) -> Template:
    templates = await tables.Templates.objects()
    return Template(template_name="pages/templates.html.jinja2", context={"templates": templates})


@get("/templates/new")
async def get_templates_new(request: HTMXRequest) -> Template:
    return Template(template_name="pages/templates-new.html.jinja2")


@post("/templates", dto=NewTemplateDTO)
async def post_template(request: HTMXRequest, data: NewTemplate) -> Template:
    template = await tables.Templates.objects().create(title=data.title)

    return HTMXTemplate(
        push_url=f"{template.id}",
        template_name="fragments/templates-view.html.jinja2",
        context={"template": template}
    )


@get("/templates/{template_id:int}")
async def get_template(request: HTMXRequest, template_id: int) -> Template:
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)
    
    return Template(template_name="pages/templates-id.html.jinja2", context={"template": template})


@put("/templates/{template_id:int}", dto=EditTemplateDTO)
async def put_template(template_id: int, data: EditTemplate) -> Template:
    template = await tables.Templates.update(title=data.title).where(tables.Templates.id == template_id)

    return Template(template_name="fragments/templates-view.html.jinja2", context={"template": ViewTemplate(template_id, data.title)})


@delete("/templates/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template(template_id: int) -> None:
    await tables.Templates.delete().where(tables.Templates.id == template_id)


@get("/templates/{template_id:int}/edit")
async def get_template_id_edit(request: HTMXRequest, template_id: int) -> Template:
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)

    return Template(template_name="fragments/templates-edit.html.jinja2", context={"template": template})


app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=["assets"]),
        get_home,
        get_templates,
        post_template,
        put_template,
        get_templates_new,
        get_template,
        delete_template,
        get_template_id_edit,
    ],
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("templates"),
        engine=JinjaTemplateEngine,
    ),
)
