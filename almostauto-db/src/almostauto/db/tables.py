from piccolo.table import Table
from piccolo.columns import ForeignKey, Integer, Varchar, Timestamptz


class Templates(Table):
    title = Varchar()
    created = Timestamptz()
    updated = Timestamptz()
    deleted = Timestamptz(null=True, default=None)
