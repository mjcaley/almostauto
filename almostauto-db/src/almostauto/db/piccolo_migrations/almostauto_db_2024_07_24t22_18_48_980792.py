from piccolo.apps.migrations.auto.migration_manager import MigrationManager


ID = "2024-07-24T22:18:48:980792"
VERSION = "1.13.1"
DESCRIPTION = ""


async def forwards():
    manager = MigrationManager(
        migration_id=ID, app_name="", description=DESCRIPTION
    )

    def run():
        print(f"running {ID}")

    manager.add_raw(run)

    return manager
