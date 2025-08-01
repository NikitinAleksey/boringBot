import json
import os.path
from pathlib import Path

from core.paths import BASE_DIR


class TextExtractor:
    def __init__(self):
        file_path = Path(BASE_DIR, 'bot', 'static', 'texts.json')
        with open(file_path, encoding="utf-8") as f:
            self._texts = json.load(f)

    def get_text(self, key: str, **kwargs) -> str:
        """
        Метод достает текст по ключу. Если переданы kwargs, они будут подставлены в текст.

        :param key: Ключ, по которому ищем.
        :param kwargs: Если переданы, будут подставлены в текст (например: {name} будет заменен реальным именем).
        :return:
        """
        text = self._texts.get(key, {}).get('text', '')
        return text.format(**kwargs) if kwargs else text

    def get_buttons(self, key: str) -> list[str] | list[list[str]]:
        """
        Метод достает текст кнопок по ключу. Если переданы kwargs, они будут подставлены в текст.

        :param key: Ключ, по которому ищем.
        :return:
        """
        buttons = self._texts.get(key, {}).get('buttons', [])
        return buttons


text_extractor = TextExtractor()
