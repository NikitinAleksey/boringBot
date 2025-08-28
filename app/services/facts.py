import random
from typing import Optional

from aiogram.fsm.context import FSMContext

from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from models.models import ItemModel, ContentModel, TranslatedContentModel
from services.interface import BaseService
from services.translator import BaseTranslator


class FactsService(BaseService):
    def __init__(self, translator: BaseTranslator, api_services: dict[str, BaseAPI],
                 repository: BaseMongoRepository):
        super().__init__(translator, api_services, repository)

    async def get_item(self, state: Optional[FSMContext] = None) -> str:
        """
        Метод получения запрашиваемого объекта. Идет либо в бд, либо в апи.

        :param state: Опциональный параметр состояния, здесь не нужен.
        :return: Текст ответа.
        """
        current_choice = random.randint(1, 5)
        #
        # if current_choice == 1:
        #     item = await self.repository.get_random_record()

        # # Тут его надо нормализовать и перевести
        api_service = self._get_service()
        # Получаем ресурс
        resource = await api_service.get_resource()
        # Првоеряем, есть ли такой в бд по ссылке на ресурс и первым символам
        first_five_words = " ".join(resource.split()[:5])
        match = {'title': first_five_words}
        own_object = await self.repository.read_one(match=match)

        # Собираем item
        if own_object:
            print('Есть в бд')
            item = self._normalize_item(resource=None, api_service=api_service, current_object=own_object)
        else:
            print('Нет в бд')
            item = self._normalize_item(resource=resource, api_service=api_service, current_object=None)
            await self.repository.create(new_resource=item)

        print(item)
        return item.translated.text

    def _normalize_item(
            self,
            resource: Optional[str],
            api_service: BaseAPI,
            current_object: Optional[dict],
    ) -> ItemModel:
        """
        Приводит полученный item к модели
        :param resource:
        :param api_service:
        :param current_object:
        :return:
        """
        if current_object:
            return ItemModel(**current_object)

        content = ContentModel(
            text=resource,
            lang='en'
        )
        translated_text = self.translator.translate(text=resource)
        translated = TranslatedContentModel(
            text=translated_text,
            translated_by='google',
        )
        title = ' '.join(resource.split(' ')[:5])
        return ItemModel(
            title=title,
            translated=translated,
            content=content,
            source=api_service.config.URL,
        )

    def _get_service(self, api_service_name: Optional[str] = None) -> BaseAPI | None:
        """
        Выбирает случайный API сервис, если не передан api_service_name или сервиса
        с api_service_name не существует.

        :param api_service_name: Опциональное имя сервиса. Если не передан.
        :return: Выбранный сервис.
        """
        api_service = None
        if api_service_name:
            api_service = self.api_services.get(api_service_name)

        return api_service if api_service_name else random.choice(list(self.api_services.values()))
