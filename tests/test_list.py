import logging
import os
import pathlib
import sqlite3

import pytest

from lists.list_manager import ListManager


logger = logging.getLogger(__name__)


def test_get_invalid_list(lists_file):
    with pytest.raises(FileNotFoundError):
        ListManager(lists_file, "fake_list")


def test_get_valid_list(lists_file):
    with sqlite3.connect(lists_file) as conn:
        conn.execute("INSERT INTO lists(list_name) VALUES('test_list')")
        conn.execute("CREATE TABLE test_list (item TEXT UNIQUE)")
        conn.commit()
    ListManager(lists_file, "test_list")


def test_has_items(lists_file):
    with sqlite3.connect(lists_file) as conn:
        conn.execute("INSERT INTO lists(list_name) VALUES('test_list')")
        conn.execute("CREATE TABLE test_list (item TEXT UNIQUE)")
        conn.commit()
    lm = ListManager(lists_file, "test_list")

    lm.add("item1")
    lm.add("item2")
    lm.add("item3")

    assert lm.has("item1")
    assert lm.has("item2")
    assert lm.has("item3")
    assert not lm.has("item4")


def test_add_items(lists_file):
    with sqlite3.connect(lists_file) as conn:
        conn.execute("INSERT INTO lists(list_name) VALUES('test_list')")
        conn.execute("CREATE TABLE test_list (item TEXT UNIQUE)")
        conn.commit()
    lm = ListManager(lists_file, "test_list")

    assert lm.add("item1")
    assert lm.add("item2")
    assert lm.add("item3")
    # logger.info(f"{lists_file=}")
    # input(lm.list_name)
    assert not lm.add("item3")


def test_remove_items(lists_file):
    with sqlite3.connect(lists_file) as conn:
        conn.execute("INSERT INTO lists(list_name) VALUES('test_list')")
        conn.execute("CREATE TABLE test_list (item TEXT UNIQUE)")
        conn.commit()
    lm = ListManager(lists_file, "test_list")
    lm.add("item1")
    lm.add("item2")
    lm.add("item3")
    lm.add("item4")
    assert lm.has("item4")
    assert lm.remove("item4")
    assert not lm.has("item4")
    assert not lm.remove("item4")
