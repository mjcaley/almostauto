from typing import Any, Mapping
from jinjax.catalog import Catalog

from litestar import MediaType, Request, get, Litestar
from litestar.response import Template

from litestar.template import TemplateProtocol, TemplateEngineProtocol
from litestar.template.config import TemplateConfig

from litestar import Litestar
from litestar.contrib.htmx.request import HTMXRequest
from litestar.static_files import create_static_files_router
from litestar.status_codes import HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

from litestar import Litestar, get

from pathlib import Path

from .templates import templates_router
from .template_steps import template_steps_router
from .runbooks import runbooks_router
from .runbook_steps import runbook_steps_router


class JinjaXTemplate(TemplateProtocol):
    def __init__(self, engine: Catalog, template_name: str):
        self.engine = engine
        self.template_name = template_name

    def render(self, **kwargs) -> str:
        return self.engine.render(self.template_name, **kwargs)


class JinjaXTemplateEngine(TemplateEngineProtocol[JinjaXTemplate, Mapping[str, Any]]):
    def __init__(self, directory=None, **kwargs):
        self.catalog = Catalog()
        self.catalog.add_folder(directory)

    def get_template(self, template_name: str) -> JinjaXTemplate:
        return JinjaXTemplate(self.catalog, template_name)


@get("/")
async def get_home() -> Template:
    return Template(template_name="HomePage", media_type=MediaType.HTML)


def http_404(_: Request, exc: Exception) -> Template:
    return Template(
        template_name="404", media_type=MediaType.HTML, status_code=HTTP_404_NOT_FOUND
    )


def http_500(_: Request, exc: Exception) -> Template:
    return Template(
        template_name="500",
        media_type=MediaType.HTML,
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
    )


app = Litestar(
    route_handlers=[
        create_static_files_router(path="/static", directories=[Path(__file__).parent / Path("static")]),
        get_home,
        templates_router,
        template_steps_router,
        runbooks_router,
        runbook_steps_router,
    ],
    exception_handlers={
        HTTP_404_NOT_FOUND: http_404,
        HTTP_500_INTERNAL_SERVER_ERROR: http_500,
    },
    template_config=TemplateConfig(
        directory=Path(__file__).parent / Path("components"),
        engine=JinjaXTemplateEngine,
    ),
    request_class=HTMXRequest,
)
