from typing import Annotated

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import MediaType, Response, Router, get, patch
from litestar.enums import RequestEncodingType
from litestar.params import Body
from litestar.exceptions import (
    NotFoundException,
    InternalServerException,
    ClientException,
)
from litestar.response import Template

from almostauto.db import tables
from .models import RunbookStepPatch


@patch("/steps/{step_number:int}")
async def patch_runbook_step(
    runbook_id: int,
    step_number: int,
    data: Annotated[RunbookStepPatch, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> Template:
    async with tables.RunbookSteps._meta.db.transaction():
        current_result = (
            await tables.RunbookSteps.select(tables.RunbookSteps.result)
            .where(
                tables.RunbookSteps.runbook == runbook_id,
                tables.RunbookSteps.number == step_number,
            )
            .first()
        )
        if current_result and current_result["result"] == data.result:
            raise ClientException(detail="Cannot trasition to same result")
        await tables.RunbookSteps.update(
            {tables.RunbookSteps.result: tables.RunbookSteps.Result(data.result)}
        ).where(
            tables.RunbookSteps.runbook == runbook_id,
            tables.RunbookSteps.number == step_number,
        )

    step = (
        await tables.RunbookSteps.objects()
        .where(
            tables.RunbookSteps.runbook == runbook_id,
            tables.RunbookSteps.number == step_number,
        )
        .first()
    )

    return Template(
        template_name="runbook_steps.ResultControl",
        context={"runbook_id": runbook_id, "step": step},
        media_type=MediaType.HTML,
    )


runbook_steps_router = Router(
    path="/runbooks/{runbook_id:int}",
    route_handlers=[
        patch_runbook_step,
    ],
)
