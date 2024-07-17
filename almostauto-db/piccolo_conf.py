from piccolo.conf.apps import AppRegistry
from piccolo.engine.postgres import PostgresEngine


DB = PostgresEngine(config={
    "host": "localhost",
    "database": "almostauto",
    "user": "postgres",
    "password": "",
})


# A list of paths to piccolo apps
# e.g. ['blog.piccolo_app']
APP_REGISTRY = AppRegistry(apps=["almostauto.db.piccolo_app"])
