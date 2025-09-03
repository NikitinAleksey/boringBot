from typing import Optional, Type

from motor.motor_asyncio import AsyncIOMotorCollection

from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from services.services_interface import BaseService
from services.translator import RealGoogleTranslator


class ServiceBuilder:
    def __init__(self):
        self._service_class: Optional[Type[BaseService]] = None
        self._api_class: Optional[Type[BaseAPI]] = None
        self._api_config: Optional[object] = None
        self._collection: Optional[AsyncIOMotorCollection] = None
        self._repo_class: Optional[Type[BaseMongoRepository]] = None
        self._translator: Optional[RealGoogleTranslator] = None # GoogleTranslator жестко вшит, так как нет нормальных альтернатив

    def with_service_class(self, service_cls: Type[BaseService]) -> "ServiceBuilder":
        self._service_class = service_cls
        return self

    def with_api(self, api_cls: Type[BaseAPI], config: object) -> "ServiceBuilder":
        self._api_class = api_cls
        self._api_config = config
        return self

    def with_repository(self, repo_cls: Type[BaseRepository], collection: AsyncIOMotorCollection) -> "ServiceBuilder":
        self._repo_class = repo_cls
        self._collection = collection
        return self

    def with_translator(self, translator: BaseTranslator) -> "ServiceBuilder":
        self._translator = translator
        return self

    def build(self) -> BaseService:
        if not all([self._service_class, self._api_class, self._repo_class, self._collection]):
            raise ValueError("Not all required components are set")

        api_service = self._api_class(config=self._api_config)
        repo_instance = self._repo_class(self._collection)

        return self._service_class(
            api_service=api_service,
            repository=repo_instance,
            translator=self._translator
        )
