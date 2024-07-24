from dataclasses import dataclass

from litestar.dto import DataclassDTO


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

NewTemplateStepDTO = DataclassDTO[NewTemplateStep]
