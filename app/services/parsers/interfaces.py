from abc import ABC, abstractmethod
from typing import Any

from models.models import QuestionModel


class BaseQuizParser(ABC):
    @abstractmethod
    def parse_object(self, data: Any, source: str) -> list[QuestionModel]:
        """
        Парсит полученный объект и приводит к нормализованному виду.

        :param data: Сырые данные.
        :param source: Источник.
        :return: Список вопросов для квиза.
        """
        pass
