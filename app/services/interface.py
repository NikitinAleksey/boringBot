from abc import ABC, abstractmethod

from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from services.translator import BaseTranslator


class BaseService(ABC):
    def __init__(
            self,
            translator: BaseTranslator,
            api_services: dict[str, BaseAPI],
            repository: BaseMongoRepository,
    ):
        self.translator = translator
        self.api_services = api_services
        self.repository = repository

    @abstractmethod
    async def get_item(self):
        """
        Основной метод получения ресурсов.
        Этот метод обязан реализовать каждый наследник.

        :return:
        """
        pass

