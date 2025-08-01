from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, FilePath, Field

from core.paths import BASE_DIR


class GoogleTranslatorConfig(BaseSettings):
    GOOGLE_TRANSLATE_API_KEY: SecretStr
    GOOGLE_APPLICATION_CREDENTIALS: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )


google_translate_config = GoogleTranslatorConfig()
