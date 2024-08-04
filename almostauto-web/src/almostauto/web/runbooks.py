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
from .models import RunbookPatch, RunbookPatchDTO


@get()
async def list_runbooks(request: HTMXRequest) -> Template:
    runbooks = await tables.Runbooks.objects()

    if request.htmx:
        return Template(
            template_name="runbooks.ListRunbooks",
            context={"runbooks": runbooks},
            media_type=MediaType.HTML,
        )
    else:
        return Template(
            template_name="RunbooksListPage",
            context={"runbooks": runbooks},
            media_type=MediaType.HTML,
        )


@get("/{runbook_id:int}")
async def runbook(request: HTMXRequest, runbook_id: int) -> Template:
    runbook = await tables.Runbooks.objects().get(tables.Runbooks.id == runbook_id)

    if request.htmx:
        return Template(
            template_name="runbooks.RunbookId",
            context={"runbook": runbook},
            media_type=MediaType.HTML,
        )
    else:
        return Template(
            template_name="RunbookIdPage",
            context={"runbook": runbook},
            media_type=MediaType.HTML,
        )


@patch("/{runbook_id:int}")
async def patch_runbook(
    runbook_id: int,
    data: Annotated[RunbookPatch, Body(media_type=RequestEncodingType.URL_ENCODED)],
) -> Template:
    async with tables.Runbooks._meta.db.transaction():
        current_result = (
            await tables.Runbooks.select(tables.Runbooks.result)
            .where(tables.Runbooks.id == runbook_id)
            .first()
        )

        if not current_result:
            raise NotFoundException(detail="Runbook ID not found")
        elif current_result[
            "result"
        ] == tables.Runbooks.Result.IN_PROGRESS and data.result in [
            tables.Runbooks.Result.NEW,
            tables.Runbooks.Result.IN_PROGRESS,
        ]:
            raise ClientException(
                detail="'In Progress' can only trasition to finished result state"
            )
        elif current_result["result"] == data.result:
            raise ClientException(detail="Cannot transition to same result state")

        await tables.Runbooks.update({tables.Runbooks.result: data.result}).where(
            tables.Runbooks.id == runbook_id
        )

    runbook = await tables.Runbooks.objects().get(tables.Runbooks.id == runbook_id)

    return Template(
        template_name="runbooks.ControlPanel",
        context={"runbook_id": runbook_id, "status": runbook.result},
    )


runbooks_router = Router(
    path="/runbooks",
    route_handlers=[
        list_runbooks,
        runbook,
        patch_runbook,
    ],
)
