from dependency_injector import containers, providers

from bot.features.menu.strategies import FactStrategy
from bot.static.text_extractor import TextExtractor
from database.respositories.repositories import MongoRepository
from dependencies.dependencies import REAL_GOOGLE_CLIENT, FREE_GOOGLE_CLIENT
from external.facts.facts import NumbersAPI
from services.facts import FactsService
from services.translator import RealGoogleTranslator, FreeGoogleTranslator


class Container(containers.DeclarativeContainer):
    config = providers.Configuration()

    # API-сервисы:
    # Facts
    numbers_api = providers.Singleton(NumbersAPI, config.api.numbers)

    api_services = {
        'numbers': numbers_api,
    }
    # Translators
    real_google_translator = providers.Singleton(RealGoogleTranslator, client=REAL_GOOGLE_CLIENT)
    free_google_translator = providers.Singleton(FreeGoogleTranslator, client=FREE_GOOGLE_CLIENT)

    # Text extractor
    text_extractor = providers.Singleton(TextExtractor, client=FREE_GOOGLE_CLIENT)

    # Repositories
    facts_repo = providers.Singleton(MongoRepository, collection=config.mongo.FACTS)
    # jokes_repo = providers.Singleton(MongoRepository, collection=config.mongo.JOKES)

    # Services
    fact_service = providers.Factory(
        FactsService,
        translator=real_google_translator,
        repository=facts_repo,
        api_services=api_services,
    )

    # Strategies
    fact_strategy = providers.Factory(FactStrategy, service=fact_service)
    # joke_strategy = providers.Factory(JokeStrategy, service=joke_service)
