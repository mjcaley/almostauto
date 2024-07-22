import asyncio

from litestar.contrib.htmx.request import HTMXRequest
from litestar import Router, get
from litestar.response import Template

from litestar import get, delete, post, put

from litestar.status_codes import HTTP_200_OK

from jinja2_fragments.litestar import HTMXBlockTemplate

from almostauto.db import tables
from .models import (
    EditTemplate,
    EditTemplateDTO,
    NewTemplate,
    NewTemplateDTO,
    ViewTemplate,
)


# region Pages


@get()
async def templates_page() -> Template:
    templates = await tables.Templates.objects()

    return Template(
        template_name="pages/templates.html.jinja2",
        context={"templates": templates},
    )


@get("/new")
async def templates_new_page() -> Template:
    return Template(template_name="pages/templates-new.html.jinja2")


@get("/{template_id:int}")
async def template_id_page(template_id: int) -> Template:
    template, steps = await asyncio.gather(
        tables.Templates.objects().get(tables.Templates.id == template_id),
        tables.TemplateSteps.objects().where(tables.TemplateSteps.id == template_id),
    )

    return Template(
        template_name="pages/templates-id.html.jinja2",
        context={"template": template, "steps": steps},
    )


# endregion


@get("/list")
async def templates_list() -> Template:
    templates = await tables.Templates.objects()

    return HTMXBlockTemplate(
        template_name="pages/templates.html.jinja2",
        context={"templates": templates},
        block_name="list",
    )


@delete("/list/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template_from_list(template_id: int) -> None:
    await tables.Templates.delete().where(tables.Templates.id == template_id)


@post(dto=NewTemplateDTO)
async def post_template(data: NewTemplate) -> Template:
    template = await tables.Templates.objects().create(title=data.title)

    return HTMXBlockTemplate(
        push_url=f"{template.id}",
        template_name="pages/templates-id.html.jinja2",
        context={"template": template, "steps": []},
        block_name="content",
    )


@put("/{template_id:int}", dto=EditTemplateDTO)
async def put_template(template_id: int, data: EditTemplate) -> Template:
    template = (
        await tables.Templates.update(title=data.title)
        .where(tables.Templates.id == template_id)
        .returning(*tables.Templates.all_columns())
    )

    return HTMXBlockTemplate(
        push_url=f"/templates/{template_id}",
        template_name="pages/templates-id.html.jinja2",
        context={"template": template, "steps": []},
        block_name="template",
    )


@delete("/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template(template_id: int) -> Template:
    await tables.Templates.delete().where(tables.Templates.id == template_id)
    templates = await tables.Templates.objects()

    return HTMXBlockTemplate(
        template_name="pages/templates.html.jinja2",
        context={"templates": templates},
        block_name="content",
    )


@get("/{template_id:int}/edit")
async def edit_template(request: HTMXRequest, template_id: int) -> Template:
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)

    if request.htmx:
        return HTMXBlockTemplate(
            push_url=f"/templates/{template_id}/edit",
            template_name="pages/templates-edit.html.jinja2",
            context={"template": template},
            block_name="template",
        )
    else:
        return Template(
            template_name="pages/templates-edit.html.jinja2",
            context={"template": template},
        )


templates_router = Router(
    path="/templates",
    route_handlers=[
        templates_page,
        templates_new_page,
        template_id_page,
        templates_list,
        delete_template_from_list,
        post_template,
        put_template,
        delete_template,
        edit_template,
    ],
)
