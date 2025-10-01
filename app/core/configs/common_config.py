from pydantic import Field
from pydantic_settings import BaseSettings

from core.configs.bot_config import BotConfig
from core.configs.database_config import MongoConfig
from core.configs.external_api_config import NumbersAPIConfig
from core.configs.ngrok_config import NgrokConfig
from core.configs.translators_configs import GoogleTranslatorConfig


class CommonConfig(BaseSettings):
    # Common api error message
    API_ERROR: str = Field(..., alias="API_ERROR")
