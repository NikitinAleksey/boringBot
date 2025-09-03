from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorCollection, AsyncIOMotorCursor
from pymongo.results import InsertOneResult

from database.respositories.interfaces import BaseMongoRepository
from models.models import ItemModel


class MongoRepository(BaseMongoRepository):
    def __init__(self, collection: AsyncIOMotorCollection):
        super().__init__(collection)

    async def insert_one(self, new_resource: dict) -> InsertOneResult:
        """
        Создает новый объект в своей коллекции.

        :param new_resource: Новый объект.
        :return: Результат вставки.
        """
        return await self.collection.insert_one(document=new_resource)

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

    async def read_many(
            self,
            match: dict = None,
            project: dict = None,
    ) -> AsyncIOMotorCursor:
        """
        Ищет объекты в своей коллекции.

        :param match: Параметры поиска.
        :param project: Проджект для возврата.
        :return: Курсор.
        """
        result = self.collection.find(filter=match)
        return result

    async def insert_many(
            self,
            query: list[dict],
    ):
        """
        Создает новые объекты в своей коллекции.

        :param query: Новый объект.
        :return: Результат вставки.
        """
        await self.collection.insert_many(documents=query)


class FactsRepository(MongoRepository):
    """Репозиторий фактов"""
    pass


class JokesRepository(MongoRepository):
    """Репозиторий шуток"""
    pass


class QuizzesRepository(MongoRepository):
    """Репозиторий результатов квизов"""
    pass


class QuizQuestionsRepository(MongoRepository):
    """Репозиторий вопросов для квизов"""
    pass
