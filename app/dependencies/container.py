from aiogram import Bot, Dispatcher
from deep_translator import GoogleTranslator
from dependency_injector import containers, providers
from google.cloud import translate_v2
from google.oauth2 import service_account

from bot.bot import BoringBot
from bot.features.menu.dispatcher import StrategyDispatcher
from bot.features.menu.strategies import FactStrategy, StartStrategy, MainMenuStrategy, JokeStrategy, QuizStrategy
from bot.fsm.states import MenuState
from bot.keyboards.builders import InlineKeyboardFactory
from bot.static.text_extractor import TextExtractor
from core.configs.bot_config import BotConfig
from core.configs.database_config import MongoConfig
from core.configs.external_api_config import NumbersAPIConfig, CatsNinjaAPIConfig, UselessFactsAPIConfig, \
    MeowFactsAPIConfig, RandomJokeAPIConfig, DadJokeAPIConfig, ChuckNorrisAPIConfig, OpenTdbAPIConfig
from core.configs.translators_configs import GoogleTranslatorConfig
from database.collections import Collections
from database.connector import MongoConnector
from database.respositories.repositories import MongoRepository
from external.facts.facts import NumbersAPI, CatsNinjaAPI, UselessFactsAPI, MeowFactsAPI
from external.jokes.jokes import RandomJokeAPI, DadJokeAPI, ChuckNorrisAPI
from external.quizzes.quizzes import OpenTdbAPI
from services.facts import FactsService
from services.jokes import JokesService
from services.parsers.open_tdb import OpenTDBParser
from services.quiz import QuizService
from services.translator import RealGoogleTranslator, FreeGoogleTranslator


class Container(containers.DeclarativeContainer):
    # TODO распилить к хуям этой контейнер + выпилить создание конфигов - конфиги создаем в конфигах, а тут только в
    #  Object суем
    config = providers.Configuration()

    bot_config = providers.Object(BotConfig())
    numbers_config = providers.Object(NumbersAPIConfig())
    translator_config = providers.Object(GoogleTranslatorConfig())
    mongo_config = providers.Object(MongoConfig())

    # API-сервисы:
    # Facts
    numbers_api = NumbersAPI(NumbersAPIConfig())
    cats_ninja = CatsNinjaAPI(CatsNinjaAPIConfig())
    dogs_facts = UselessFactsAPI(UselessFactsAPIConfig())
    meow_facts = MeowFactsAPI(MeowFactsAPIConfig())

    api_facts_services = {
            'numbers': numbers_api,
            'cats_ninja': cats_ninja,
            'dogs_facts': dogs_facts,
            'meow_facts': meow_facts,
        }

    # Jokes
    # random_joke_api = RandomJokeAPI(RandomJokeAPIConfig()) # TODO хуета поганая, выпилить
    dad_joke_api = DadJokeAPI(DadJokeAPIConfig())
    chuck_norris_joke_api = ChuckNorrisAPI(ChuckNorrisAPIConfig())

    api_jokes_services = {
        # 'random_joke_api': random_joke_api,
        'dad_joke_api': dad_joke_api,
        'chuck_norris_joke_api': chuck_norris_joke_api,
    }

    # Quizzes
    open_tdb_api = OpenTdbAPI(OpenTdbAPIConfig())

    api_quizzes_services = {
        'open_tdb_api': open_tdb_api,
    }
    # Ngrok
    # ngrok = providers.Singleton(LaunchNgrok, config=ngrok_config)
    # Translators setup:
    # Google credentials
    credentials = service_account.Credentials.from_service_account_file(
        filename=GoogleTranslatorConfig().CREDENTIALS,
    )

    # Clients
    real_google_client = translate_v2.Client(credentials=credentials)
    free_google_client = GoogleTranslator(source='auto', target='ru')

    # Translators
    real_google_translator = RealGoogleTranslator(client=real_google_client)
    free_google_translator = FreeGoogleTranslator(client=free_google_client)

    # Text extractor
    text_extractor = TextExtractor()

    # Database
    # Connection
    connector = providers.Singleton(MongoConnector, uri=mongo_config().get_uri())

    # Collections
    collections = Collections()
    facts_collection = collections.get_collection(
        connection=connector().get_connection(), db_name=mongo_config().DB_NAME, collection_name=mongo_config().FACTS,
    )
    jokes_collection = collections.get_collection(
        connection=connector().get_connection(), db_name=mongo_config().DB_NAME, collection_name=mongo_config().JOKES,
    )
    quizzes_collection = collections.get_collection(
        connection=connector().get_connection(), db_name=mongo_config().DB_NAME, collection_name=mongo_config().QUIZZES,
    )

    # Repositories
    facts_repo = MongoRepository(collection=facts_collection)
    jokes_repo = MongoRepository(collection=jokes_collection)
    quizzes_repo = MongoRepository(collection=quizzes_collection)

    # Keyboards
    inline_keyboard = InlineKeyboardFactory()

    # Services
    fact_service = providers.Object(FactsService(
        translator=real_google_translator,
        repository=facts_repo,
        api_services=api_facts_services,
        )
    )

    jokes_service = providers.Object(JokesService(
        translator=real_google_translator,
        repository=jokes_repo,
        api_services=api_jokes_services,
        )
    )

    quizzes_service = providers.Object(QuizService(
        translator=real_google_translator,
        repository=quizzes_repo,
        api_services=api_quizzes_services,
        parser=OpenTDBParser(),
        )
    )
    # Strategies
    start_strategy = providers.Object(StartStrategy(
        keyboard_factory=inline_keyboard,
        text_extractor=text_extractor,
        )
    )
    main_menu_strategy = providers.Object(MainMenuStrategy(
        keyboard_factory=inline_keyboard,
        text_extractor=text_extractor,
        )
    )
    fact_strategy = providers.Object(FactStrategy(
        service=fact_service(),
        keyboard_factory=inline_keyboard,
        text_extractor=text_extractor,
        )
    )

    joke_strategy = providers.Object(
        JokeStrategy(
            service=jokes_service(),
            keyboard_factory=inline_keyboard,
            text_extractor=text_extractor,
        )
    )

    quiz_strategy = providers.Object(
        QuizStrategy(
            service=quizzes_service(),
            keyboard_factory=inline_keyboard,
            text_extractor=text_extractor,
        )
    )

    strategies = {
        MenuState.start: start_strategy,
        MenuState.main: main_menu_strategy,
        MenuState.fact: fact_strategy,
        MenuState.joke: joke_strategy,
        MenuState.quiz: quiz_strategy,
    }

    # StrategyDispatcher
    strategy_dispatcher = providers.Singleton(StrategyDispatcher, strategies=strategies)

    # Telegram Bot
    bot = providers.Singleton(
        BoringBot,
        bot=providers.Factory(
            Bot,
            token=bot_config().BOT_TOKEN.get_secret_value(),
        ),
        dp=providers.Factory(Dispatcher)
    )
