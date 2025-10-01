from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class TranslatedContentModel(BaseModel):
    text: str = Field(description='Переведённый текст контента')
    file_url: Optional[str] = Field(default=None, description='Ссылка на переведённый файл (если есть)')
    translated_by: Optional[str] = Field(default="google", description='Источник перевода')
    answers: Optional[list[str]] = Field(default_factory=list, description='Переведенные ответы, если это квиз')


class ContentModel(BaseModel):
    text: str = Field(description='Оригинальный текст контента')
    file_url: Optional[str] = Field(default=None, description='Ссылка на оригинальный файл')
    lang: Optional[str] = Field(default='en', description='Язык оригинала')


class ItemModel(BaseModel):
    title: str = Field(description='Название')
    content: ContentModel = Field(description='Оригинальное содержимое')
    translated: Optional[TranslatedContentModel] = Field(default=None, description='Переведённое содержимое')
    topics: Optional[list[str]] = Field(default_factory=list, description='Список тем айтема')
    source: Optional[str] = Field(default_factory=list, description='Источник (например, имя API)')


class QuestionModel(ItemModel):
    answers: list[str] = Field(default_factory=list, description='Список всех ответов на вопрос')
    correct_answer: str = Field(description='Правильный ответ')
    user_answer: Optional[str] = Field(default=None, description='Ответ пользователя')
    is_correct: Optional[bool] = Field(default=None, description='Флаг, показывающий, верный ли ответ дал пользователь')


class QuizModel(BaseModel):
    questions: list[QuestionModel] = Field(description='Список вопросов')
    start_time: datetime = Field(description='Время начала квиза')
    finish_time: Optional[datetime] = Field(default=None, description='Время окончания квиза')
    answered_count: int = Field(default=0, description='Всего ответов')
    correct_count: int = Field(default=0, description='Правильных ответов')


class UserQuizModel(BaseModel):
    user_tg_id: int = Field(description='TG ID пользователя.')
    quiz: QuizModel = Field(description='Данные квиза')
