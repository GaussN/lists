import logging

import pytest

from lists.list_manager import ListManager
from lists.exceptions import ListNotFound


logger = logging.getLogger(__name__)


def test_get_invalid_list(lists_file):
    with pytest.raises(ListNotFound):
        ListManager(lists_file, "fake_list")


def test_get_valid_list(lists_file, list_manager):
    ListManager(lists_file, list_manager.list_name)


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
