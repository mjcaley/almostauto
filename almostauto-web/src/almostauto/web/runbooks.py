from litestar.contrib.htmx.request import HTMXRequest
from litestar.contrib.htmx.response import HTMXTemplate
from litestar import MediaType, Response, Router, get
from litestar.exceptions import NotFoundException
from litestar.response import Template

from almostauto.db import tables


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


runbooks_router = Router(
    path="/runbooks",
    route_handlers=[
        list_runbooks,
        runbook,
    ]
)
