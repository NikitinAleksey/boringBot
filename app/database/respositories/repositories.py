from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection
from pymongo.results import InsertOneResult

from database.respositories.interfaces import BaseMongoRepository
from models.models import ItemModel


class MongoRepository(BaseMongoRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def create(self, new_resource: ItemModel) -> InsertOneResult:
        """
        Создает новый объект в своей коллекции.

        :param new_resource: Новый объект.
        :return: Результат вставки.
        """
        return await self.collection.insert_one(document=new_resource.model_dump())

    async def read_one(
            self,
            match: dict = None,
            project: dict = None,
    ) -> dict | None:
        """
        Ищет объект в своей коллекции.

        :param match: Параметры поиска.
        :param project: Проджект для возврата.
        :return: Словарь объекта (если найден) или None.
        """
        result = await self.collection.find_one(filter=match)
        return result

    async def update(self):
        pass

    async def delete(self):
        pass

    async def get_random_record(self):
        pass
