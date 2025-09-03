import logging
import os
import pathlib

import pytest

from lists.exceptions import (
    InvalidListname,
    ListAlreadyExists,
    ListIsNotEmpty,
    ListNotFound,
)
from lists.list_manager import ListManager


logger = logging.getLogger(__name__)


def test_get_invalid_list(lists_path):
    with pytest.raises(ListNotFound):
        ListManager(lists_path / "fake_list.list")


def test_get_valid_list(list_path):
    ListManager(list_path)


def test_find_item(list_path):
    list_path.write_text("item1\nitem2\nitem3\n")
    lm = ListManager(list_path)

    assert 0 == lm._ListManager__has("item1")
    assert 6 == lm._ListManager__has("item2")
    assert 12 == lm._ListManager__has("item3")
    assert -1 == lm._ListManager__has("item4")


def test_has_items(list_path):
    list_path.write_text("item1\nitem2\nitem3\n")

    lm = ListManager(list_path)

    assert lm.has("item1")
    assert lm.has("item2")
    assert lm.has("item3")
    assert not lm.has("item4")


def test_add_items(list_path):
    lm = ListManager(list_path)
    assert lm.add("item1")
    assert lm.add("item2")
    assert lm.add("item3")
    assert not lm.add("item3")
    assert list_path.read_text() == "item1\nitem2\nitem3\n"


def test_remove_items(list_path):
    lm = ListManager(list_path)
    lm.add("item1")
    lm.add("item2")
    lm.add("item3")
    lm.add("item4")
    assert lm.has("item4")
    assert lm.remove("item4")
    assert not lm.has("item4")
    assert not lm.remove("item4")
