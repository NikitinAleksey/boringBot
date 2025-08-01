from pydantic import BaseModel
from core.configs.bot_config import BotConfig
from core.configs.ngrok_config import NgrokConfig
from core.configs.external_api_config import NumbersAPIConfig
from core.configs.translators_configs import GoogleTranslatorConfig


class MainConfig(BaseModel):
    bot: BotConfig
    ngrok: NgrokConfig
    numbers: NumbersAPIConfig

    class Config:
        arbitrary_types_allowed = True


main_config = MainConfig(
    bot=BotConfig(),
    ngrok=NgrokConfig(),
    numbers=NumbersAPIConfig(),
)
