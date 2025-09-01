# abcdefghijklmnopqrstuvwxyz
import os
import pathlib
import shutil

import pytest


@pytest.fixture
def lists_path(tmp_path) -> pathlib.Path:
    _lists_path = tmp_path / "lists"
    _lists_path.mkdir()
    yield _lists_path
    shutil.rmtree(_lists_path)
    tmp_path.rmdir()


@pytest.fixture
def list_path(lists_path) -> pathlib.Path:
    _list_path = lists_path / "test.list"
    _list_path.open("wt").close()
    yield _list_path
    if _list_path.exists():
        os.unlink(_list_path)
