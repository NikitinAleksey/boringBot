from abc import ABC, abstractmethod
from typing import Union, Optional

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.features.menu.models import BotResponse
from bot.keyboards.builders import BaseKeyboardFactory
from bot.static.text_extractor import TextExtractor
from external.interface import BaseAPI
from services.interface import BaseService


class BaseStrategy(ABC):
    """Базовый интерфейс стратегий меню."""
    def __init__(
            self,
            keyboard_factory: BaseKeyboardFactory,
            text_extractor: TextExtractor,
            service: Optional[BaseService] = None,
    ):
        self.keyboard_factory = keyboard_factory
        self.text_extractor = text_extractor
        self.service = service

    @abstractmethod
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
    ) -> BotResponse:
        """
        Все потомки обязаны реализовать этот метод.

        :param event: Событие в боте.
        :returns: Ответ пользователю.
        """
        pass


class StartStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
    ) -> BotResponse:
        """
        Стратегия отображения меню по нажатию кнопки старт.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :returns: Ответ пользователю.
        """
        print('StartStrategy')
        name = event.from_user.first_name
        text = self.text_extractor.get_text(key="start", name=name)
        buttons = self.text_extractor.get_buttons(key="start")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class MainMenuStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
    ) -> BotResponse:
        """
        Стратегия отображения главного меню.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :returns: Ответ пользователю.
        """
        print('MainMenuStrategy')
        name = event.from_user.first_name
        text = self.text_extractor.get_text(key="main_menu", name=name)
        buttons = self.text_extractor.get_buttons(key="main_menu")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class FactStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
    ) -> BotResponse:
        """
        Стратегия отображения получения интересного факта. Факт получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :returns: Ответ пользователю.
        """
        print('FactStrategy')
        name = event.from_user.first_name
        preview_text = self.text_extractor.get_text(key="fact", name=name)
        main_text = await self.service.get_item()
        text = preview_text + '\n\n' + main_text
        buttons = self.text_extractor.get_buttons(key="fact")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class JokeStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
    ) -> BotResponse:
        """
        Стратегия отображения получения шуток. Шутку получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :returns: Ответ пользователю.
        """
        print('JokeStrategy')
        name = event.from_user.first_name
        preview_text = self.text_extractor.get_text(key="joke", name=name)
        main_text = await self.service.get_item()
        text = preview_text + '\n\n' + main_text
        buttons = self.text_extractor.get_buttons(key="joke")
        kb = self.keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)
