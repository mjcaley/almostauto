from litestar import MediaType, Router, get
from litestar.response import Template
from litestar.contrib.htmx.response import HTMXTemplate

from litestar import get, delete, post, put

from litestar.status_codes import HTTP_200_OK

from piccolo.query import Max

from almostauto.db import tables
from .models import (
    EditTemplateStep,
    EditTemplateStepDTO,
    NewTemplateStepDTO,
    NewTemplateStep,
)


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
        latest_number = (
            await tables.TemplateSteps.select(Max(tables.TemplateSteps.number))
            .where(tables.TemplateSteps.template == template_id)
            .first()
        )
        next_number = (
            (latest_number["max"] + 1) if latest_number["max"] is not None else 0
        )
        await tables.TemplateSteps.objects().create(
            title=data.title, template=template_id, number=next_number
        )
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .order_by(tables.TemplateSteps.number)
    )

    return Template(
        template_name="template_steps.CreateTemplateStep",
        context={"steps": steps, "template_id": template_id},
        media_type=MediaType.HTML,
    )


@delete("/{number:int}", status_code=HTTP_200_OK)
async def delete_template_step(template_id: int, number: int) -> Template:
    async with tables.TemplateSteps._meta.db.transaction():
        await tables.TemplateSteps.delete().where(
            tables.Templates.id == template_id and tables.TemplateSteps.number == number
        )
        await tables.TemplateSteps.update(
            {tables.TemplateSteps.number: tables.TemplateSteps.number - 1}
        ).where(tables.TemplateSteps.number > number)
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .order_by(tables.TemplateSteps.number)
    )

    return Template(
        template_name="template_steps.TemplateStepsList",
        context={"template_id": template_id, "steps": steps},
        media_type=MediaType.HTML,
    )


@get("/{number:int}/edit")
async def template_step_edit_form(template_id: int, number: int) -> Template:
    step = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .where(tables.TemplateSteps.number == number)
        .first()
    )

    return Template(
        template_name="template_steps.EditForm",
        context={"template_id": template_id, "step": step},
        media_type=MediaType.HTML,
    )


@put("/{number:int}", dto=EditTemplateStepDTO)
async def template_steps_edit_save(
    template_id: int, number: int, data: EditTemplateStep
) -> Template:
    await (
        tables.TemplateSteps.update({tables.TemplateSteps.title: data.title})
        .where(tables.TemplateSteps.template == template_id)
        .where(tables.TemplateSteps.number == number)
    )
    steps = (
        await tables.TemplateSteps.objects()
        .where(tables.TemplateSteps.template == template_id)
        .order_by(tables.TemplateSteps.number)
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
        template_step_edit_form,
        template_steps_edit_save,
    ],
)
