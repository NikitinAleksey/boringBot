from abc import ABC, abstractmethod

from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from services.translator import BaseTranslator


class BaseService(ABC):
    def __init__(
            self,
            translator: BaseTranslator,
            api_service: BaseAPI,
            repository: BaseMongoRepository,
    ):
        self.translator = translator
        self.api_service = api_service
        self.repository = repository

    @abstractmethod
    async def get_item(self):
        """
        Основной метод получения ресурсов.
        Этот метод обязан реализовать каждый наследник.

        :return:
        """
        pass

