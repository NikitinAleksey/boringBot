import pytest

from models.models import QuestionModel


@pytest.mark.asyncio
async def test_parse_questions(
        fixture_parser_open_tdb,
        fixture_questions,
):
    result = fixture_parser_open_tdb.parse_object(data=fixture_questions, source='test_open_tdb_url')
    assert isinstance(result, list)
    assert all(isinstance(question, QuestionModel) for question in result)
    assert len(result) == len(fixture_questions['results'])
