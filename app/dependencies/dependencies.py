import random

from aiogram import Bot, Dispatcher
from deep_translator import GoogleTranslator
from fastapi import Request
from google.cloud import translate_v2
from google.oauth2 import service_account
from motor.motor_asyncio import AsyncIOMotorCollection

from bot.bot import BoringBot
from bot.features.menu.dispatcher import StrategyDispatcher
from bot.features.menu.strategies import MainMenuStrategy, StartStrategy, FactStrategy
from bot.fsm.states import MenuState
from bot.keyboards.builders import InlineKeyboardFactory
from bot.middlewares.strategy import StrategyMiddleware
from bot.static.text_extractor import TextExtractor
from core.configs.bot_config import BotConfig
from core.configs.common_config import CommonConfig
from core.configs.database_config import MongoConfig
from core.configs.external_api_config import NumbersAPIConfig
from core.configs.ngrok_config import NgrokConfig
from core.configs.translators_configs import GoogleTranslatorConfig
from database.connector import MongoConnector
from database.respositories.repositories import MongoRepository
from external.facts.facts import NumbersAPI
from external.interface import BaseAPI
from ngrok.launcher import LaunchNgrok
from bot.routes import get_bot_routers
from services.facts import FactsService
from services.translator import (RealGoogleTranslator, FreeGoogleTranslator,
                                 BaseTranslator)


# -------------------------------- Strategies ---------------------------------
STRATEGIES = {
    MenuState.start: StartStrategy(),
    MenuState.main: MainMenuStrategy(),
    MenuState.fact: FactStrategy(),
}


# ---------------------------------- Configs ----------------------------------
BOT_CONFIG = BotConfig()
NUMBERS_CONFIG = NumbersAPIConfig()
NGROK_CONFIG = NgrokConfig()
GOOGLE_TRANSLATOR_CONFIG = GoogleTranslatorConfig()
COMMON_CONFIG = CommonConfig() # Пока пустой, может выпилю
MONGO_CONFIG = MongoConfig()

CONFIGS = {
    'bot': BOT_CONFIG,
    'ngrok': NGROK_CONFIG,
    'api': {
        'numbers': NUMBERS_CONFIG,
    },
    'google_translator': GOOGLE_TRANSLATOR_CONFIG,
    'mongo': MONGO_CONFIG,
}

API_CONFIGS = {
    NumbersAPI: NUMBERS_CONFIG,
}


# -------------------------------- Translators --------------------------------
REAL_GOOGLE_CLIENT = translate_v2.Client(
    credentials=service_account.Credentials.from_service_account_file(
        filename=GOOGLE_TRANSLATOR_CONFIG.CREDENTIALS,
    )
)
FREE_GOOGLE_CLIENT = GoogleTranslator(source='auto', target='ru')


# -------------------------------- External API -------------------------------
API_SERVICES = {NumbersAPI}


# --------------------------------- Databases ---------------------------------
MONGO_URI = CONFIGS['mongo'].get_uri()
MONGO_REPOSITORY = MongoRepository
COLLECTIONS = {
    MenuState.fact: MONGO_CONFIG.FACTS,
    MenuState.joke: MONGO_CONFIG.JOKES,
    MenuState.video: MONGO_CONFIG.VIDEOS,
}

# ----------------------------------- Utils -----------------------------------
TEXT_EXTRACTOR = TextExtractor()


# --------------------------------- Services ---------------------------------
SERVICE_MAP = {
    MenuState.fact: {
        'db_name': MONGO_CONFIG.DB_NAME,
        "collection_name": MONGO_CONFIG.FACTS,
        "api_services": API_SERVICES,
        "api_configs": API_CONFIGS,
        "repository": MONGO_REPOSITORY,
        "service": FactsService,
    },
    MenuState.joke: {
        ...
    },
}

# TODO продолжить наводить порядок
def get_translator(translator_name: str) -> BaseTranslator:
    return translators.get(translator_name)

async def get_collection(
    db_name: str,
    collection_name: str,
    mongo_uri: str,
) -> AsyncIOMotorCollection:
    connector = MongoConnector(uri=mongo_uri)
    client = await connector.get_connection()
    db = client[db_name]
    return db[collection_name]

def get_api_config(api_service: type[BaseAPI]):
    return API_CONFIGS.get(api_service)


def get_config(name: str):
    return CONFIGS.get(name)


def get_ngrok() -> LaunchNgrok:
    ngrok_config = get_config(name='ngrok')
    instance = LaunchNgrok(config=ngrok_config)
    return instance


def create_bot() -> BoringBot:
    bot_config = get_config(name='bot')
    bot = Bot(token=bot_config.BOT_TOKEN.get_secret_value())
    dp = Dispatcher()
    return BoringBot(bot=bot, dp=dp)


async def setup_bot(bot_instance: BoringBot) -> None:
    routers = get_bot_routers()
    middlewares = [
        StrategyMiddleware(await get_strategy_dispatcher()),
    ]
    bot_instance.register_routers(routers=routers)
    bot_instance.register_middlewares(middlewares=middlewares)


def get_bot_from_app(request: Request) -> BoringBot:
    return request.app.state.boring_bot


async def get_strategy_dispatcher() -> StrategyDispatcher:
    return StrategyDispatcher(
        strategies=STRATEGIES,
        keyboard_factory=InlineKeyboardFactory(),
        text_extractor=TEXT_EXTRACTOR,
        service=await get_fact_service(), # TODO тут поменять, выбор должен основываться по нажатой кнопке (факт, шутка и тд), а пока хардкодом вшито
    )


def get_random_api_service():
    print('Выбираем апи конфиг')
    configs = [NumbersAPIConfig]
    config = random.choice(configs)
    print(f'Config is: {config}')
    return NumbersAPI(config=config())


async def get_fact_service():
    api_service = get_random_api_service()
    # dn_name =
    return FactsService(
        api_service=api_service,
        # translator=google_translator, # пока жестко вшит, тестим
        translator=get_translator(translator_name='free_google_client'), # TODO тут пока чтобы не жечь лимиты
        repository=None # TODO поменять, когда реализую
    )

