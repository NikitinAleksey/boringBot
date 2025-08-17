from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr

from core.paths import BASE_DIR


class NgrokConfig(BaseSettings):
    NGROK_AUTHTOKEN: SecretStr
    NGROK_PORT: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR.parent.parent / '.env',
        env_file_encoding='utf-8',
        extra='ignore',
    )
