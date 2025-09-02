# abcdefghijklmnopqrstuvwxyz
import os
import pathlib
import shutil
import sqlite3

import pytest


@pytest.fixture
def lists_path(tmp_path) -> pathlib.Path:
    _lists_path = tmp_path / "lists"
    _lists_path.mkdir()
    yield _lists_path
    shutil.rmtree(_lists_path)
    tmp_path.rmdir()


@pytest.fixture
def lists_file(lists_path) -> pathlib.Path:
    _path = lists_path / ".lists.db"
    with sqlite3.connect(_path) as conn:
        conn.executescript("CREATE TABLE IF NOT EXISTS lists( list_name TEXT UNIQUE )")
        conn.commit()
    yield _path
    os.remove(_path)