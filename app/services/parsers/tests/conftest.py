import json
from typing import Any

import pytest
from pathlib import Path

from services.parsers.open_tdb import OpenTDBParser
from tests.conftest import open_file

_current_dir = Path(__file__).parent


@pytest.fixture
def fixture_parser_open_tdb():
    instance = OpenTDBParser()
    return instance


@pytest.fixture
def fixture_questions():
    path = _current_dir / 'data' / 'questions.json'
    data = open_file(file_path=path)
    return data
