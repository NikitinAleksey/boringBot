import html
from abc import ABC, abstractmethod
from typing import Union

from deep_translator import GoogleTranslator
from google.cloud import translate_v2


TranslatorClientType = Union[GoogleTranslator, translate_v2.Client]


class BaseTranslator(ABC):
    def __init__(self, client: TranslatorClientType):
        self.client = client

    @abstractmethod
    def translate(self, text: str, target_lang: str = "ru") -> str:
        """
        Абстрактный метод, который обязан реализовать каждый наследник.

        :param text: Текст для перевода.
        :param target_lang: На какой язык переводим.
        :return: Переведенный текст.
        """
        pass


class RealGoogleTranslator(BaseTranslator):
    def __init__(self, client: translate_v2.Client):
        super().__init__(client)

    def translate(self, text: str, target_lang: str = "ru") -> str:
        result = self.client.translate(text, target_language=target_lang)
        return html.unescape(result["translatedText"])


class FreeGoogleTranslator(BaseTranslator):
    def __init__(self, client: GoogleTranslator):
        super().__init__(client)

    def translate(self, text: str, target_lang: str = "ru") -> str:
        return self.client.translate(text, target=target_lang)
