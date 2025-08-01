from typing import Optional

from pydantic import BaseModel, Field


class TranslatedContentModel(BaseModel):
    text: str = Field(description='Переведённый текст контента')
    file_url: Optional[str] = Field(default=None, description='Ссылка на переведённый файл (если есть)')
    translated_by: Optional[str] = Field(default="google", description='Источник перевода')


class ContentModel(BaseModel):
    text: str = Field(description='Оригинальный текст контента')
    file_url: Optional[str] = Field(default=None, description='Ссылка на оригинальный файл')
    lang: Optional[str] = Field(default='en', description='Язык оригинала')


class ItemModel(BaseModel):
    title: str = Field(description='Название')
    content: ContentModel = Field(description='Оригинальное содержимое')
    translated: Optional[TranslatedContentModel] = Field(description='Переведённое содержимое')
    topics: Optional[list[str]] = Field(default_factory=list, description='Список тем айтема')
    source: Optional[str] = Field(default_factory=list, description='Источник (например, имя API)')
