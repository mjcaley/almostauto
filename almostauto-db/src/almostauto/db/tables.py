from piccolo.table import Table
from piccolo.columns import ForeignKey, Integer, Varchar, Timestamptz, OnDelete


class Templates(Table):
    title = Varchar()
    created = Timestamptz()
    updated = Timestamptz()
    deleted = Timestamptz(null=True, default=None)


class TemplateSteps(Table):
    order = Integer()
    title = Varchar()
    template = ForeignKey(Templates, null=False, on_delete=OnDelete.no_action)
