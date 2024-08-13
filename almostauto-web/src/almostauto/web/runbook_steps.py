import datetime
from typing import Annotated

from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar.dto import DTOData
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
from .models import RunbookStepPatch, RunbookStepPatchDTO


@patch("/{step_number:int}", dto=RunbookStepPatchDTO)
async def patch_runbook_step(
    runbook_id: int,
    step_number: int,
    # data: DTOData[tables.RunbookSteps]
    data: Annotated[DTOData[tables.RunbookSteps], Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> Template:
    async with tables.RunbookSteps._meta.db.transaction():
        step = (
                await tables.RunbookSteps.objects().where(
                tables.RunbookSteps.runbook == runbook_id,
                tables.RunbookSteps.number == step_number,
            )
            .first())
        current_result = step.result

        data.update_instance(step)

        if current_result == tables.RunbookSteps.Result.NOT_STARTED:
            step.started = datetime.datetime.now(datetime.UTC)
        elif current_result in [
            tables.RunbookSteps.Result.SUCCESS,
            tables.RunbookSteps.Result.SKIPPED,
            tables.RunbookSteps.Result.FAILED,
        ]:
            step.finished = datetime.datetime.now(datetime.UTC)

        await step.save([tables.RunbookSteps.result, tables.RunbookSteps.title])

    step = (
        await tables.RunbookSteps.objects()
        .where(
            tables.RunbookSteps.runbook == runbook_id,
            tables.RunbookSteps.number == step_number,
        )
        .first()
    )

    return Template(
        template_name="runbook_steps.Step",
        context={"runbook_id": runbook_id, "step": step},
        media_type=MediaType.HTML,
    )


@get("/{step_number:int}/edit")
async def edit_step_form(runbook_id: int, step_number: int) -> Template:
    step = await tables.RunbookSteps.objects().get(
        tables.RunbookSteps.runbook == runbook_id
        and tables.RunbookSteps.number == step_number
    )

    return Template(
        template_name="runbook_steps.EditForm",
        context={"runbook_id": runbook_id, "step": step},
    )


runbook_steps_router = Router(
    path="/runbooks/{runbook_id:int}/steps",
    route_handlers=[
        patch_runbook_step,
        edit_step_form,
    ],
)
