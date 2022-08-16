from peewee import Model
from playhouse.pool import PooledPostgresqlExtDatabase

from sm_api.settings import DATABASE

db = PooledPostgresqlExtDatabase(
    DATABASE["database"],
    host=DATABASE["host"],
    max_connections=200,
    stale_timeout=300,
    user=DATABASE["username"],
    password=DATABASE["password"]
)


class BaseModel(Model):
    class Meta:
        database = db
