from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from core.paths import BASE_DIR


class CommonConfig(BaseSettings):

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
