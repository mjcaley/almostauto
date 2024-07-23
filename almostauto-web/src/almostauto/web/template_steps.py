from litestar.contrib.htmx.request import HTMXRequest
from litestar import Router, get
from litestar.response import Template

from litestar import get, delete, post, put

from litestar.status_codes import HTTP_200_OK

from jinja2_fragments.litestar import HTMXBlockTemplate

from almostauto.db import tables


@post()
async def new_template_step(template_id: int) -> Template:
    ...


@get()
async def template_steps(template_id: int) -> str:
    template = await tables.Templates.objects().where(tables.Templates.id == template_id)
    steps = await tables.TemplateSteps.objects().where(tables.TemplateSteps.template.id == template_id)

    return HTMXBlockTemplate(
        template_name="pages/templates-id.html.jinja2",
        context={"steps": steps, "template": template},
        block_name="template_steps",
    )


template_steps_router = Router(
    path="/templates/{template_id:int}/steps",
    route_handlers=[
        template_steps,
        new_template_step,
    ]
)
