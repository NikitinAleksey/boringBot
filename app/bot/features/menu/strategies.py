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
    @abstractmethod
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            keyboard_factory: BaseKeyboardFactory,
            state: FSMContext,
            text_extractor: TextExtractor,
            service: BaseService,
    ) -> BotResponse:
        """
        Все потомки обязаны реализовать этот метод.

        :param event: Событие в боте.
        :param keyboard_factory: Фабрика клавиатуры.
        :param state: Текущее состояние в боте.
        :param text_extractor: Экземпляр класса с текстами.
        :param service: Экземпляр класса работы с внешними сервисами.
        :returns: Ответ пользователю.
        """
        pass


class StartStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            keyboard_factory: BaseKeyboardFactory,
            state: FSMContext,
            text_extractor: TextExtractor,
            service: Optional[BaseService] = None,
    ) -> BotResponse:
        """
        Стратегия отображения меню по нажатию кнопки старт.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param keyboard_factory: Фабрика клавиатуры.
        :param state: Текущее состояние в боте.
        :param text_extractor: Экземпляр класса с текстами.
        :param service: Экземпляр класса работы с внешними сервисами.
        :returns: Ответ пользователю.
        """
        print('StartStrategy')
        name = event.from_user.first_name
        text = text_extractor.get_text(key="start", name=name)
        buttons = text_extractor.get_buttons(key="start")
        kb = keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class MainMenuStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            keyboard_factory: BaseKeyboardFactory,
            state: FSMContext,
            text_extractor: TextExtractor,
            service: Optional[BaseService] = None,
    ) -> BotResponse:
        """
        Стратегия отображения главного меню.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param keyboard_factory: Фабрика клавиатуры.
        :param state: Текущее состояние в боте.
        :param text_extractor: Экземпляр класса с текстами.
        :param service: Экземпляр класса работы с внешними сервисами.
        :returns: Ответ пользователю.
        """
        print('MainMenuStrategy')
        name = event.from_user.first_name
        text = text_extractor.get_text(key="main_menu", name=name)
        buttons = text_extractor.get_buttons(key="main_menu")
        kb = keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)


class FactStrategy(BaseStrategy):
    async def execute(
            self,
            event: Union[Message, CallbackQuery],
            keyboard_factory: BaseKeyboardFactory,
            state: FSMContext,
            text_extractor: TextExtractor,
            service: BaseService,
    ) -> BotResponse:
        """
        Стратегия отображения получения интересного факта. Факт получает из своего сервиса.
        Достает тексты и кнопки и возвращает мх.

        :param event: Событие в боте.
        :param keyboard_factory: Фабрика клавиатуры.
        :param state: Текущее состояние в боте.
        :param text_extractor: Экземпляр класса с текстами.
        :param service: Экземпляр класса работы с внешними сервисами.
        :returns: Ответ пользователю.
        """
        print('FactStrategy')
        name = event.from_user.first_name
        preview_text = text_extractor.get_text(key="fact", name=name)
        main_text = await service.get_item()
        text = preview_text + '\n\n' + main_text
        buttons = text_extractor.get_buttons(key="fact")
        kb = keyboard_factory.create(buttons=buttons, adjust=1)
        return BotResponse(text=text, kb=kb)
