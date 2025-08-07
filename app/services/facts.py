from database.respositories.interfaces import BaseMongoRepository
from external.interface import BaseAPI
from models.models import ItemModel, ContentModel, TranslatedContentModel
from services.interface import BaseService
from services.translator import BaseTranslator


class FactsService(BaseService):
    def __init__(self, translator: BaseTranslator, api_service: BaseAPI,
                 repository: BaseMongoRepository):
        super().__init__(translator, api_service, repository)

    async def get_item(self) -> str:
        """
        Метод получения запрашиваемого объекта. Идет либо в бд, либо в апи.
        :return: Текст ответа.
        """
        # current_choice = random.randint(1, 5)
        #
        # if current_choice == 1:
        #     item = await self.repository.get_random_record()
        #
        # else:
        #     # А тут идем в наш сервис апи
        #     item = await self.api_service.get_resource()
        #     # Потом записываем новый ресурс бд
        #
        # # Тут его надо нормализовать и перевести

        # Получаем ресурс
        resource = await self.api_service.get_resource()
        # Првоеряем, есть ли такой в бд по ссылке на ресурс и первым символам
        has_already = await self.repository.read_one()
        # Собираем item
        item = self._normalize_item(resource=resource)

        # TODO где-то тут отправляем в бд - рэбит может подрубить?
        from pprint import pprint
        pprint(item.dict())
        return item.translated.text

    def _normalize_item(self, resource: str) -> ItemModel:
        """
        Приводит полученный item к модели
        :param resource:
        :return:
        """
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
            source=self.api_service.config.URL,
        )



