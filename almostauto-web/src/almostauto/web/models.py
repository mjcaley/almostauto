from dataclasses import dataclass

from litestar.dto import DataclassDTO, DTOConfig
from litestar.contrib.piccolo import PiccoloDTO
from almostauto.db import tables


@dataclass
class NewTemplate:
    title: str


@dataclass
class EditTemplate:
    title: str


@dataclass
class ViewTemplate:
    id: int
    title: str


NewTemplateDTO = DataclassDTO[NewTemplate]
EditTemplateDTO = DataclassDTO[EditTemplate]
ViewTemplateDTO = DataclassDTO[ViewTemplate]


@dataclass
class NewTemplateStep:
    title: str


@dataclass
class EditTemplateStep:
    title: str


NewTemplateStepDTO = DataclassDTO[NewTemplateStep]
EditTemplateStepDTO = DataclassDTO[EditTemplateStep]


@dataclass
class RunbookPatch:
    result: int


RunbookPatchDTO = DataclassDTO[RunbookPatch]


@dataclass
class RunbookStepPatch:
    title: str
    result: int


class RunbookStepPatchDTO(PiccoloDTO[tables.RunbookSteps]):
    config = DTOConfig(partial=True)
