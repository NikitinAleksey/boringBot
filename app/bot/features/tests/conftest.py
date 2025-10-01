import json
from typing import Any

import pytest
from pathlib import Path

from tests.conftest import open_file

_current_dir = Path(__file__).parent


# @pytest.fixture
# def fixture_