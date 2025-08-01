from abc import ABC, abstractmethod

from core.configs.external_api_config import BaseAPIConfig


class BaseAPI(ABC):
    def __init__(self, config: BaseAPIConfig):
        self.config = config

    @abstractmethod
    async def get_resource(self):
        """
        Каждый наследник обязан реализовать данный метод.

        :return:
        """
        pass
