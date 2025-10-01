from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject

from bot.features.menu.dispatcher import StrategyDispatcher


class StrategyMiddleware(BaseMiddleware):
    def __init__(self, strategy_dispatcher: StrategyDispatcher):
        super().__init__()
        self.strategy_dispatcher = strategy_dispatcher

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
        data['strategy_dispatcher'] = self.strategy_dispatcher
        result = await handler(event, data)
        return result
