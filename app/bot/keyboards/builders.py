from abc import ABC, abstractmethod

from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


class BaseKeyboardFactory(ABC):
    @staticmethod
    @abstractmethod
    def create(buttons: list[str] | list[tuple[str, str]], adjust: int):
        pass


class InlineKeyboardFactory(BaseKeyboardFactory):
    @staticmethod
    def create(buttons: list[list[str, str]], adjust: int = 2) -> InlineKeyboardMarkup:
        """
        Создает inline-клавиатуру.

        :param buttons: Список кортежей (текст, callback_data)
        :param adjust: Кол-во колонок.
        :return: InlineKeyboardMarkup
        """
        builder = InlineKeyboardBuilder()
        for text, callback in buttons:
            builder.button(text=text, callback_data=callback)
        builder.adjust(adjust)
        return builder.as_markup()


class ReplyKeyboardFactory(BaseKeyboardFactory):
    @staticmethod
    def create(buttons: list[str], adjust: int = 1) -> ReplyKeyboardMarkup:
        """
        Создает reply-клавиатуру.

        :param buttons: Список названий кнопок.
        :param adjust: Кол-во колонок.
        :return: ReplyKeyboardMarkup
        """
        builder = ReplyKeyboardBuilder()
        for text in buttons:
            builder.button(text=text)
        builder.adjust(adjust)
        return builder.as_markup(resize_keyboard=True, one_time_keyboard=False)
