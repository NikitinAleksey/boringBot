import asyncio
from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.fsm.storage.base import BaseStorage
from aiogram.types import TelegramObject, Message


class ClearMessagesMiddleware(BaseMiddleware):
    # TODO пока не использовать, надо продумать план, как корректно удалять сообщения - только лишь удалять, или еще редактировать
    def __init__(self, storage: BaseStorage):
        super().__init__()
        self.storage = storage

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Обработка события и передача данных в хранилище.

        :param handler: Обработчик события.
        :param event: Событие Telegram.
        :param data: Данные, передаваемые в обработчик.
        :return: Результат выполнения обработчика.
        """
        # event.
        chat_id = (
            event.message.chat.id
            if isinstance(event, Message)
            else event.callback_query.message.chat.id
        )
        # if self.storage.get(chat_id):
        #     while not self.storage[chat_id].empty():
        #         event_to_be_cleaned = await self.storage[chat_id].get()
        #         try:
        #             await event_to_be_cleaned.delete()
        #         except AttributeError as exc:
        #             self.log.warning(f"Чат: {chat_id}. Ошибка: {exc}.")
        # else:
        #     self.storage[chat_id] = asyncio.Queue()
        #
        # if isinstance(event.message, Message):
        #     await self.storage[chat_id].put(event.message)
        #

        print(chat_id)
        result = await handler(event, data)
        #
        # if result:
        #     await self.storage[chat_id].put(result)
        return result
