import random

from aiogram import Bot, Dispatcher
from fastapi import Request

from bot.bot import BoringBot
from bot.features.menu.dispatcher import StrategyDispatcher
from bot.features.menu.strategies import MainMenuStrategy, StartStrategy, FactStrategy
from bot.fsm.states import MenuState
from bot.keyboards.builders import InlineKeyboardFactory
from bot.middlewares.strategy import StrategyMiddleware
from bot.static.text_extractor import text_extractor
from core.configs.external_api_config import NumbersAPIConfig
from core.configs.translators_configs import google_translate_config
from dependencies.configs_map import configs
from external.facts.facts import NumbersAPI
from ngrok.launcher import LaunchNgrok

from bot.routes import get_bot_routers
from services.facts import FactsService
from services.translator import GoogleTranslator, translator


google_translator = GoogleTranslator(config=google_translate_config)

strategies = {
    MenuState.start: StartStrategy(),
    MenuState.main: MainMenuStrategy(),
    MenuState.fact: FactStrategy(),
    # MenuState.fact: MainMenuStrategy(), # TODO изменить классы
    # MenuState.youtube: MainMenuStrategy(),
}


def get_config(name: str):
    return configs.get(name)


def get_ngrok() -> LaunchNgrok:
    ngrok_config = get_config(name='ngrok')
    instance = LaunchNgrok(config=ngrok_config)
    return instance


def create_bot() -> BoringBot:
    bot_config = get_config(name='bot')
    bot = Bot(token=bot_config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    return BoringBot(bot=bot, dp=dp)


def setup_bot(bot_instance: BoringBot) -> None:
    routers = get_bot_routers()
    middlewares = [
        StrategyMiddleware(get_strategy_dispatcher()),
    ]
    bot_instance.register_routers(routers=routers)
    bot_instance.register_middlewares(middlewares=middlewares)


def get_bot_from_app(request: Request) -> BoringBot:
    return request.app.state.boring_bot


def get_strategy_dispatcher() -> StrategyDispatcher:
    return StrategyDispatcher(
        strategies=strategies,
        keyboard_factory=InlineKeyboardFactory(),
        text_extractor=text_extractor,
        service=get_fact_service(), # TODO тут поменять, выбор должен основываться по нажатой кнопке (факт, шутка и тд), а пока хардкодом вшито
    )


def get_random_api_service():
    print('Выбираем апи конфиг')
    api_configs = [NumbersAPIConfig]
    config = random.choice(api_configs)
    print(f'Config is: {config}')
    return NumbersAPI(config=config())


def get_fact_service():
    api_service = get_random_api_service()

    return FactsService(
        api_service=api_service,
        # translator=google_translator, # пока жестко вшит, тестим
        translator=translator, # TODO тут пока чтобы не жечь лимиты
        repository=None # TODO поменять, когда реализую
    )
