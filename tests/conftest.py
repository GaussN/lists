import os
import pathlib
import shutil

import pytest

from lists.list_manager import ListManager
from lists.lists_manager import ListsManager


@pytest.fixture
def lists_path(tmp_path) -> pathlib.Path:
    _lists_path = tmp_path / "lists"
    _lists_path.mkdir()
    yield _lists_path
    shutil.rmtree(_lists_path)
    tmp_path.rmdir()


@pytest.fixture
def lists_manager(lists_path) -> ListsManager:
    _lsm = ListsManager(lists_path)
    yield _lsm


@pytest.fixture
def list_manager(lists_manager) -> ListManager:
    _lm = lists_manager.create("test.list")
    yield _lm
