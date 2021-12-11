from umongo.frameworks import MotorAsyncIOInstance
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core import settings


class _MongoConnection:
    client: AsyncIOMotorClient = None
    instance: MotorAsyncIOInstance = MotorAsyncIOInstance()

    @property
    def database(self) -> AsyncIOMotorDatabase:
        if self.client:
            return self.client[settings.mongodb_database]

    def connect(self):
        if not self.client:
            connection.client = AsyncIOMotorClient(settings.mongodb_uri)
            connection.instance.set_db(connection.database)

    def close(self):
        connection.client.close()


connection = _MongoConnection()
