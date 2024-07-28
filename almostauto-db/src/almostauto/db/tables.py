from enum import StrEnum
from piccolo.table import Table
from piccolo.columns import ForeignKey, Integer, Varchar, Timestamptz, OnDelete


class Templates(Table):
    title = Varchar()
    created = Timestamptz()
    updated = Timestamptz()
    deleted = Timestamptz(null=True, default=None)


class TemplateSteps(Table):
    number = Integer()
    title = Varchar()
    template = ForeignKey(Templates, null=False, on_delete=OnDelete.cascade)


class Runbooks(Table):
    class Result(StrEnum):
        NEW = "New"
        SUCCESS = "Success"
        FAILED = "Failed"
        CANCELLED = "Cancelled"

    title = Varchar()
    result = Varchar(length=25, choices=Result, default=Result.NEW)
    completed = Timestamptz(null=True)
    created = Timestamptz()
    updated = Timestamptz()


class RunbookSteps(Table):
    number = Integer()
    title = Varchar()
    runbook = ForeignKey(Runbooks)
