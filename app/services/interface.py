from abc import ABC, abstractmethod
from typing import Optional

from aiogram.fsm.context import FSMContext

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
    async def get_item(self, state: Optional[FSMContext] = None):
        """
        Основной метод получения ресурсов.
        Этот метод обязан реализовать каждый наследник.

        :param state: Опциональный параметр состояния,
        нужен не для всех сервисов.
        :return:
        """
        pass

