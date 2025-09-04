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


def test_get_valid_list(list_manager):
    ListManager(list_manager.list_path)


def test_find_item(list_manager):
    list_manager.add("item1")
    list_manager.add("item2")
    list_manager.add("item3")
    assert 0 == list_manager._ListManager__has("item1")
    assert 6 == list_manager._ListManager__has("item2")
    assert 12 == list_manager._ListManager__has("item3")
    assert -1 == list_manager._ListManager__has("item4")


def test_has_items(list_manager):
    list_manager.add("item1")
    list_manager.add("item2")
    list_manager.add("item3")
    assert list_manager.has("item1")
    assert list_manager.has("item2")
    assert list_manager.has("item3")
    assert not list_manager.has("item4")


def test_add_items(list_manager):
    assert list_manager.add("item1")
    assert list_manager.add("item2")
    assert list_manager.add("item3")
    assert not list_manager.add("item3")


def test_remove_items(list_manager):
    list_manager.add("item1")
    list_manager.add("item2")
    list_manager.add("item3")
    list_manager.add("item4")
    assert list_manager.has("item4")
    assert list_manager.remove("item4")
    assert not list_manager.has("item4")
    assert not list_manager.remove("item4")
