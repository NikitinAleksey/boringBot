from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure


class MongoConnector:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, uri: str):
        if not hasattr(self, '_client'):
            self._uri = uri
            self._client = AsyncIOMotorClient(self._uri)

    async def is_alive(self) -> bool:
        try:
            await self._client.admin.command("ping")
            return True
        except ConnectionFailure:
            return False

    def reconnect(self):
        self._client = AsyncIOMotorClient(self._uri)

    def get_connection(self) -> AsyncIOMotorClient:
        return self._client

    def close_connection(self):
        if self._client:
            self._client.close()
