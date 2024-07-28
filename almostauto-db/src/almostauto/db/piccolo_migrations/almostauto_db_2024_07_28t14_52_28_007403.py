from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from enum import Enum
from piccolo.columns.base import OnDelete
from piccolo.columns.base import OnUpdate
from piccolo.columns.column_types import ForeignKey
from piccolo.columns.column_types import Integer
from piccolo.columns.column_types import Serial
from piccolo.columns.column_types import Timestamptz
from piccolo.columns.column_types import Varchar
from piccolo.columns.defaults.timestamptz import TimestamptzNow
from piccolo.columns.indexes import IndexMethod
from piccolo.table import Table


class Runbooks(Table, tablename="runbooks", schema=None):
    id = Serial(
        null=False,
        primary_key=True,
        unique=False,
        index=False,
        index_method=IndexMethod.btree,
        choices=None,
        db_column_name="id",
        secret=False,
    )


ID = "2024-07-28T14:52:28:007403"
VERSION = "1.13.1"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="almostauto-db", description=DESCRIPTION
    )

    manager.add_table(
        class_name="RunbookSteps",
        tablename="runbook_steps",
        schema=None,
        columns=None,
    )

    manager.add_table(
        class_name="Runbooks", tablename="runbooks", schema=None, columns=None
    )

    manager.add_column(
        table_class_name="RunbookSteps",
        tablename="runbook_steps",
        column_name="number",
        db_column_name="number",
        column_class_name="Integer",
        column_class=Integer,
        params={
            "default": 0,
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="RunbookSteps",
        tablename="runbook_steps",
        column_name="title",
        db_column_name="title",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="RunbookSteps",
        tablename="runbook_steps",
        column_name="runbook",
        db_column_name="runbook",
        column_class_name="ForeignKey",
        column_class=ForeignKey,
        params={
            "references": Runbooks,
            "on_delete": OnDelete.cascade,
            "on_update": OnUpdate.cascade,
            "target_column": None,
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Runbooks",
        tablename="runbooks",
        column_name="title",
        db_column_name="title",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 255,
            "default": "",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Runbooks",
        tablename="runbooks",
        column_name="result",
        db_column_name="result",
        column_class_name="Varchar",
        column_class=Varchar,
        params={
            "length": 25,
            "default": "New",
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": Enum(
                "Result",
                {
                    "NEW": "New",
                    "SUCCESS": "Success",
                    "FAILED": "Failed",
                    "CANCELLED": "Cancelled",
                },
            ),
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Runbooks",
        tablename="runbooks",
        column_name="completed",
        db_column_name="completed",
        column_class_name="Timestamptz",
        column_class=Timestamptz,
        params={
            "default": TimestamptzNow(),
            "null": True,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Runbooks",
        tablename="runbooks",
        column_name="created",
        db_column_name="created",
        column_class_name="Timestamptz",
        column_class=Timestamptz,
        params={
            "default": TimestamptzNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.add_column(
        table_class_name="Runbooks",
        tablename="runbooks",
        column_name="updated",
        db_column_name="updated",
        column_class_name="Timestamptz",
        column_class=Timestamptz,
        params={
            "default": TimestamptzNow(),
            "null": False,
            "primary_key": False,
            "unique": False,
            "index": False,
            "index_method": IndexMethod.btree,
            "choices": None,
            "db_column_name": None,
            "secret": False,
        },
        schema=None,
    )

    manager.alter_column(
        table_class_name="TemplateSteps",
        tablename="template_steps",
        column_name="template",
        db_column_name="template",
        params={"on_delete": OnDelete.cascade},
        old_params={"on_delete": OnDelete.no_action},
        column_class=ForeignKey,
        old_column_class=ForeignKey,
        schema=None,
    )

    return manager
