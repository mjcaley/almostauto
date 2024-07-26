from litestar import MediaType, Router, get
from litestar.response import Template
from litestar.contrib.htmx.response import HTMXTemplate

from litestar import get, delete, post, put

from litestar.status_codes import HTTP_200_OK

from piccolo.query import Max

from almostauto.db import tables
from .models import NewTemplateStepDTO, NewTemplateStep


@get()
async def template_steps(template_id: int) -> Template:
    steps = await tables.TemplateSteps.objects().where(
        tables.TemplateSteps.template.id == template_id
    )

    return Template(
        template_name="template_steps.TemplateStepsList",
        context={"steps": steps, "template_id": template_id},
        media_type=MediaType.HTML,
    )


@get("/new")
async def new_template_step_form(template_id: int) -> Template:
    return Template(
        template_name="template_steps.NewTemplateStepForm",
        context={"template_id": template_id},
        media_type=MediaType.HTML,
    )


@post(dto=NewTemplateStepDTO)
async def new_template_step(template_id: int, data: NewTemplateStep) -> Template:
    async with tables.TemplateSteps._meta.db.transaction():
        latest_order = await tables.TemplateSteps.select(
            Max(tables.TemplateSteps.order)
        ).first()
        next_order = latest_order["max"] if latest_order["max"] is not None else 0
        await tables.TemplateSteps.objects().create(
            title=data.title, template=template_id, order=next_order
        )
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .order_by(tables.TemplateSteps.order)
    )

    return Template(
        template_name="template_steps.CreateTemplateStep",
        context={"steps": steps, "template_id": template_id},
        media_type=MediaType.HTML,
    )


@delete("/{order:int}", status_code=HTTP_200_OK)
async def delete_template_step(template_id: int, order: int) -> Template:
    async with tables.TemplateSteps._meta.db.transaction():
        deleted_rows = (
            await tables.TemplateSteps.delete()
            .where(
                tables.Templates.id == template_id
                and tables.TemplateSteps.order == order
            )
            .returning(tables.TemplateSteps.order)
        )
        for row in deleted_rows:
            await tables.TemplateSteps.update(
                {tables.TemplateSteps.order: tables.TemplateSteps.order - 1}
            ).where(tables.TemplateSteps.order > row["order"])
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .order_by(tables.TemplateSteps.order)
    )

    return Template(
        template_name="template_steps.TemplateStepsList",
        context={"template_id": template_id, "steps": steps},
        media_type=MediaType.HTML,
    )


template_steps_router = Router(
    path="/templates/{template_id:int}/steps",
    route_handlers=[
        template_steps,
        new_template_step,
        new_template_step_form,
        delete_template_step,
    ],
)
