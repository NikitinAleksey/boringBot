import pytest
from pathlib import Path

from services.parsers.tests.conftest import fixture_parser_open_tdb
from services.quiz import QuizService
from tests.conftest import fixture_open_tdb_api_service

_current_dir = Path(__file__).parent


@pytest.fixture
def fixture_api_services(fixture_open_tdb_api_service):
    api_services = {
        'open_tdb_api': fixture_open_tdb_api_service,
    }
    return api_services


@pytest.fixture
def fixture_quiz_services(
        fixture_api_services,
        fixture_translator,
        fixture_questions_repository,
        fixture_quizzes_repository,
        fixture_parser_open_tdb,
):
    instance = QuizService(
        translator=fixture_translator,
        api_services=fixture_api_services,
        repository=fixture_questions_repository,
        quiz_repository=fixture_quizzes_repository,
        parser=fixture_parser_open_tdb,
    )
    return instance
