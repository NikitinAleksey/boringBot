from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor

from models.models import ItemModel


class BaseMongoRepository(ABC):
    def __init__(self, collection: AsyncIOMotorCollection):
        self.collection = collection

    @abstractmethod
    async def insert_one(self, new_resource: dict):
        pass

    @abstractmethod
    async def read_one(
            self,
            match: dict = None,
            project: dict = None,
    ) -> dict | None:
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def read_many(
            self,
            match: dict = None,
            project: dict = None,
    ) -> AsyncIOMotorCursor:
        pass

    @abstractmethod
    async def insert_many(
            self,
            query: list[dict],
    ):
        pass
