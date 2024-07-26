import asyncio

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import MediaType, Router, get
from litestar.exceptions import NotFoundException
from litestar.response import Template

from litestar import get, delete, post, put

from litestar.status_codes import HTTP_200_OK, HTTP_404_NOT_FOUND

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
        template_name="TemplatesListPage",
        context={"templates": templates},
        media_type=MediaType.HTML,
    )


@get("/new")
async def templates_new_page() -> Template:
    return Template(template_name="NewTemplatePage", media_type=MediaType.HTML)


@get("/{template_id:int}")
async def template_id_page(template_id: int) -> Template:
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template)
        .order_by(tables.TemplateSteps.number)
    )

    if not template:
        raise NotFoundException()

    return Template(
        template_name="ViewTemplatePage",
        context={"template": template, "steps": steps},
        media_type=MediaType.HTML,
    )


# endregion


@get("/list")
async def templates_list() -> Template:
    templates = await tables.Templates.objects()

    return HTMXTemplate(
        template_name="templates.TemplateList",
        context={"templates": templates},
        media_type=MediaType.HTML,
    )


@delete("/list/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template_from_list(template_id: int) -> None:
    await tables.Templates.delete().where(tables.Templates.id == template_id)


@post(dto=NewTemplateDTO)
async def post_template(data: NewTemplate) -> Template:
    template = await tables.Templates.objects().create(title=data.title)

    return HTMXTemplate(
        push_url=f"{template.id}",
        template_name="templates.ViewTemplateAndSteps",
        context={"template": template, "steps": []},
        media_type=MediaType.HTML,
    )


@put("/{template_id:int}", dto=EditTemplateDTO)
async def put_template(template_id: int, data: EditTemplate) -> Template:
    await tables.Templates.update(title=data.title).where(
        tables.Templates.id == template_id
    )
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)

    return HTMXTemplate(
        push_url=f"/templates/{template_id}",
        template_name="templates.ViewTemplate",
        context={"template": template},
    )


@delete("/{template_id:int}", status_code=HTTP_200_OK)
async def delete_template(template_id: int) -> Template:
    async with tables.Templates._meta.db.transaction():
        await tables.TemplateSteps.delete().where(
            tables.TemplateSteps.template == template_id
        )
        await tables.Templates.delete().where(tables.Templates.id == template_id)
    templates = await tables.Templates.objects()

    return HTMXTemplate(
        template_name="templates.TemplatesList",
        context={"templates": templates},
    )


@get("/{template_id:int}/edit")
async def edit_template(request: HTMXRequest, template_id: int) -> Template:
    template = await tables.Templates.objects().get(tables.Templates.id == template_id)

    if request.htmx:
        return HTMXTemplate(
            push_url=f"/templates/{template_id}/edit",
            template_name="templates.EditTemplateForm",
            context={"template": template},
            media_type=MediaType.HTML,
        )
    else:
        return Template(
            template_name="EditTemplatePage",
            context={"template": template},
            media_type=MediaType.HTML,
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
