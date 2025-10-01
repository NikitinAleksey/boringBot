from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from core.paths import BASE_DIR


class BotConfig(BaseSettings):
    BOT_TOKEN: SecretStr

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
