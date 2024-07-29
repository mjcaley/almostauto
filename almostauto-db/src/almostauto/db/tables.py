from enum import IntEnum
from piccolo.table import Table
from piccolo.columns import ForeignKey, Integer, Varchar, Timestamptz, OnDelete, Text


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
    class Result(IntEnum):
        NEW = 0
        SUCCESS = 1
        FAILED = 2
        CANCELLED = 3

    title = Varchar()
    result = Integer(choices=Result, default=Result.NEW)
    completed = Timestamptz(null=True)
    created = Timestamptz()
    updated = Timestamptz()


class RunbookSteps(Table):
    class Result(IntEnum):
        NOT_STARTED = 0
        IN_PROGRESS = 1
        SUCCESS = 2
        SKIPPED = 3
        FAILED = 4

    number = Integer()
    title = Varchar()
    result = Integer(choices=Result, default=Result.NOT_STARTED)
    started = Timestamptz(null=True)
    finished = Timestamptz(null=True)
    runbook = ForeignKey(Runbooks)


class RunbookStepComment(Table):
    comment = Text()
    created = Timestamptz()
    updated = Timestamptz()
    runbook_step= ForeignKey(RunbookSteps)
