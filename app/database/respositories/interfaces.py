from abc import ABC, abstractmethod

from motor.motor_asyncio import AsyncIOMotorClient


class BaseMongoRepository(ABC):
    def __init__(self, connection: AsyncIOMotorClient):
        self.connection = connection

    @abstractmethod
    async def create(self):
        pass

    @abstractmethod
    async def read(self):
        pass

    @abstractmethod
    async def update(self):
        pass

    @abstractmethod
    async def delete(self):
        pass

    @abstractmethod
    async def get_random_record(self):
        pass
