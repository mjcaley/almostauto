from piccolo.apps.migrations.auto.migration_manager import MigrationManager
from piccolo.columns.base import OnDelete
from piccolo.columns.column_types import ForeignKey
from piccolo.table import Table


ID = "2024-07-26T22:08:27:210049"
VERSION = "1.13.1"
DESCRIPTION = "Add delete cascade to template_steps"


class RawTable(Table):
    ...


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="almostauto-db", description=DESCRIPTION
    )

    async def run_forward():
        await RawTable.raw("""
            alter table "template_steps"
            drop constraint "template_steps_template_fkey",
            add constraint "template_steps_template_fkey"
                foreign key ("template")
            references "templates"(id)
            on delete cascade
            on update cascade;
            """)
        
    manager.add_raw(run_forward)

    async def run_backward():
        await RawTable.raw("""
            alter table "template_steps"
            drop constraint "template_steps_template_fkey",
            add constraint "template_steps_template_fkey"
                foreign key ("template")
            references "templates"(id)
            on update cascade;
            """)
        
    manager.add_raw_backwards(run_backward)

    return manager
