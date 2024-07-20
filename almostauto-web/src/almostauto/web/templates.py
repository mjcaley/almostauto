import asyncio

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import get
from litestar.response import Redirect, Template

from litestar import Controller, get, delete, post, put

from litestar.status_codes import HTTP_200_OK, HTTP_302_FOUND

from almostauto.db import tables
from .models import (
    EditTemplate,
    EditTemplateDTO,
    NewTemplate,
    NewTemplateDTO,
    ViewTemplate,
)


class TemplatesController(Controller):
    path = "/templates"

    @get()
    async def get_templates(request: HTMXRequest) -> Template:
        templates = await tables.Templates.objects()
        return Template(
            template_name="pages/templates.html.jinja2",
            context={"templates": templates},
        )

    @delete(status_code=HTTP_200_OK)
    async def delete_template_from_list(self, template_id: int) -> None:
        await tables.Templates.delete().where(tables.Templates.id == template_id)

    @get("/new")
    async def get_templates_new(request: HTMXRequest) -> Template:
        return Template(template_name="pages/templates-new.html.jinja2")

    @post(dto=NewTemplateDTO)
    async def post_template(request: HTMXRequest, data: NewTemplate) -> Template:
        template = await tables.Templates.objects().create(title=data.title)

        return HTMXTemplate(
            push_url=f"{template.id}",
            template_name="fragments/templates-view.html.jinja2",
            context={"template": template, "steps": []},
        )

    @get("/{template_id:int}")
    async def get_template(request: HTMXRequest, template_id: int) -> Template:
        template, steps = await asyncio.gather(
            tables.Templates.objects().get(tables.Templates.id == template_id),
            tables.TemplateSteps.objects().where(tables.TemplateSteps.id == template_id)
        )

        return Template(
            template_name="pages/templates-id.html.jinja2",
            context={"template": template, "steps": steps},
        )

    @put("/{template_id:int}", dto=EditTemplateDTO)
    async def put_template(self, template_id: int, data: EditTemplate) -> Template:
        template = await tables.Templates.update(title=data.title).where(
            tables.Templates.id == template_id
        )

        return HTMXTemplate(
            push_url=f"/templates/{template_id}",
            template_name="fragments/templates-view.html.jinja2",
            context={"template": ViewTemplate(template_id, data.title), "steps": []},
        )

    @delete("/{template_id:int}", status_code=HTTP_200_OK)
    async def delete_template(request: HTMXRequest, template_id: int) -> Template:
        await tables.Templates.delete().where(tables.Templates.id == template_id)
        templates = await tables.Templates.objects()

        return Template(
            template_name="fragments/templates-list.html.jinja2",
            context={"template": templates}
        )

    @get("/{template_id:int}/edit")
    async def get_template_id_edit(request: HTMXRequest, template_id: int) -> Template:
        template = await tables.Templates.objects().get(
            tables.Templates.id == template_id
        )

        return HTMXTemplate(
            push_url=f"/templates/{template_id}/edit",
            template_name="fragments/templates-edit.html.jinja2",
            context={"template": template},
        )
