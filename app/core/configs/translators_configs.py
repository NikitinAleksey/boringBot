from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, FilePath, Field

from core.paths import BASE_DIR


class BaseTranslatorConfig(BaseSettings):
    API_KEY: Optional[str] = Field(default=None, description='Ключ АПИ если необходим')
    CREDENTIALS: Optional[str] = Field(default=None, description='Путь до файла с кредами ,если необходимы')

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


class GoogleTranslatorConfig(BaseTranslatorConfig):
    API_KEY: SecretStr = Field(alias='GOOGLE_TRANSLATE_API_KEY')
    CREDENTIALS: str = Field(alias='GOOGLE_APPLICATION_CREDENTIALS')
