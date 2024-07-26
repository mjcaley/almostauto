from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-07-26T14:43:44:297879"
VERSION = "1.13.1"
DESCRIPTION = "Rename template_steps.order column to number"


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="almostauto-db", description=DESCRIPTION
    )

    manager.rename_column(
        table_class_name="TemplateSteps",
        tablename="template_steps",
        old_column_name="order",
        new_column_name="number",
        old_db_column_name="order",
        new_db_column_name="number",
        schema=None,
    )

    return manager
