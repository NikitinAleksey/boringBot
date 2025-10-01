import pytest

from tests.conftest import (
    fixture_fsm_state, fixture_open_tdb_config, fixture_translator,
    fixture_questions_repository, fixture_questions_collection,
    fixture_collections, fixture_connector, fixture_mongo_config,
    fixture_quizzes_repository, fixture_quizzes_collection,
)
from services.parsers.tests.conftest import fixture_questions


@pytest.mark.asyncio
async def test_quiz_service(
        fixture_quiz_services,
        fixture_fsm_state,
        fixture_open_tdb_config,
        fixture_questions,
        fixture_translator,
        fixture_questions_repository,
        fixture_questions_collection,
        fixture_collections,
        fixture_connector,
        fixture_mongo_config,
        fixture_quizzes_repository,
        fixture_quizzes_collection,
):
    fixture_fsm_state.clear()
    fixture_fsm_state.set_data({})
    expected_questions_len = len(fixture_questions.get('results'))
    await fixture_quiz_services.get_item(state=fixture_fsm_state)

    data = await fixture_fsm_state.get_data()
    assert data.get('question_index') == 0
    questions_len = len(data.get('quiz').get('questions'))
    assert questions_len == expected_questions_len
    assert not data.get('finished')

    for i in range(1, questions_len):
        await fixture_quiz_services.get_item(state=fixture_fsm_state)
        data = await fixture_fsm_state.get_data()
        assert data.get('question_index') == i
        assert not data.get('finished')

    await fixture_quiz_services.get_item(state=fixture_fsm_state)
    data = await fixture_fsm_state.get_data()
    assert data.get('finished')
