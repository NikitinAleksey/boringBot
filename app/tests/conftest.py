import json
from typing import Any
from unittest.mock import MagicMock, AsyncMock

import pytest
from pathlib import Path

from aiogram.fsm.context import FSMContext
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.storage.memory import MemoryStorage

from core.configs.database_config import MongoConfig
from core.configs.external_api_config import OpenTdbAPIConfig
from database.collections import Collections
from database.connector import MongoConnector
from database.respositories.repositories import QuizQuestionsRepository, QuizzesRepository
from external.quizzes.quizzes import OpenTdbAPI
from services.translator import RealGoogleTranslator


def open_file(file_path: Path) -> Any:
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


@pytest.fixture
def fixture_translator():
    client = MagicMock()
    translator = RealGoogleTranslator(client=client)
    translator.translate = MagicMock(
        side_effect=[
            val
            for i in range(10)
            for val in (
                "Переведённый текст вопроса",
                "<A0>Ответ1</A0><A1>Ответ2</A1><A2>Ответ3</A2><A3>Ответ4</A3>",
            )
        ]
    )
    return translator


@pytest.fixture
def fixture_open_tdb_config():
    config = OpenTdbAPIConfig(OPEN_TDB_URL='open_tdb_mock_url.com')
    return config


@pytest.fixture
def fixture_open_tdb_api_service(
        fixture_open_tdb_config,
        fixture_questions,
):
    instance = OpenTdbAPI(config=fixture_open_tdb_config)
    instance.get_resource = AsyncMock(return_value=fixture_questions)
    return instance


@pytest.fixture
def fixture_collections():
    instance = Collections()
    return instance


@pytest.fixture
def fixture_mongo_config():
    config = MongoConfig(
        MONGO_INITDB_ROOT_USERNAME='fake_user',
        MONGO_INITDB_ROOT_PASSWORD='fake_pass',
        MONGO_HOST='fake_host',
        MONGO_PORT=9999,
        DB_NAME='fake_db_name',
        FACTS='fake_facts',
        JOKES='fake_jokes',
        VIDEOS='fake_videos',
        QUIZZES='fake_quizzes',
        QUESTIONS='fake_questions',
    )
    return config


@pytest.fixture
def fixture_connector(fixture_mongo_config):
    uri = fixture_mongo_config.get_uri()
    instance = MongoConnector(uri=uri)
    instance.get_connection = MagicMock()
    return instance


@pytest.fixture
def fixture_questions_collection(
        fixture_collections,
        fixture_connector,
        fixture_mongo_config,
):
    collection = fixture_collections.get_collection(
        db_name=fixture_mongo_config.DB_NAME,
        collection_name=fixture_mongo_config.QUESTIONS,
        connection=fixture_connector.get_connection(),
    )
    return collection


@pytest.fixture
def fixture_quizzes_collection(
        fixture_collections,
        fixture_connector,
        fixture_mongo_config,
):
    collection = fixture_collections.get_collection(
        db_name=fixture_mongo_config.DB_NAME,
        collection_name=fixture_mongo_config.QUIZZES,
        connection=fixture_connector.get_connection(),
    )
    return collection


@pytest.fixture
def fixture_questions_repository(fixture_questions_collection):
    repository = QuizQuestionsRepository(collection=fixture_questions_collection)
    repository.insert_many = AsyncMock()
    return repository


@pytest.fixture
def fixture_quizzes_repository(fixture_quizzes_collection):
    repository = QuizzesRepository(collection=fixture_quizzes_collection)
    return repository


@pytest.fixture
def fixture_fsm_state():
    storage = MemoryStorage()
    key = StorageKey(
        chat_id=11111,
        user_id=11111,
        bot_id=999,
    )
    state = FSMContext(storage=storage, key=key)
    return state
