import pytest

from lists.exceptions import (
    InvalidListname,
    ListAlreadyExists,
    ListIsNotEmpty,
    ListNotFound,
)
from lists.lists_manager import ListsManager


def test_incorrect_police(lists_path):
    with pytest.raises(ValueError):
        ListsManager(lists_path, "uncorrect_policy")


@pytest.mark.parametrize("policy", ("raise", "hide"))
def test_correct_policy(lists_path, policy):
    ListsManager(lists_path, policy)


def test_incorrect_path():
    with pytest.raises(FileNotFoundError):
        ListsManager("fake_path", "raise")


def test_getitem_invalid(lists_manager):
    with pytest.raises(ListNotFound):
        lists_manager["fake.list"]


def test_get_invalid(lists_manager):
    assert lists_manager.get("fake.test") is None


def test_getitem_valid(lists_manager, list_manager):
    lm = lists_manager[list_manager.list_name]
    assert lm.list_name == list_manager.list_name


def test_get_valid(lists_manager, list_manager):
    lm = lists_manager.get(list_manager.list_name)
    assert lm is not None
    assert lm.list_name == list_manager.list_name


def test_create(lists_manager):
    lm = lists_manager.create("new.list", raise_if_exists=True)
    assert lm.list_name == "new.list"


def test_create_exists_raise(lists_manager, list_manager):
    with pytest.raises(ListAlreadyExists):
        lm = lists_manager.create(list_manager.list_name, raise_if_exists=True)


def test_create_exists_ignore(lists_manager, list_manager):
    lm = lists_manager.create(list_manager.list_name, raise_if_exists=False)
    assert lm.list_name == list_manager.list_name


def test_remove_empty(lists_manager, list_manager):
    lists_manager.remove(list_manager.list_name)


def test_remove_not_empty(lists_manager, list_manager):
    lm = lists_manager[list_manager.list_name]
    lm.add("item1")
    with pytest.raises(ListIsNotEmpty):
        lists_manager.remove(list_manager.list_name)


def test_remove_not_empty_force(lists_manager, list_manager):
    lists_manager.remove(list_manager.list_name, force=True)


def test_remove_non_exists_ignore(lists_manager):
    lists_manager.remove("fake.list", raise_if_not_exists=False)


def test_remove_non_exists_raise(lists_manager):
    with pytest.raises(ListNotFound):
        lists_manager.remove("fake.list", raise_if_not_exists=True)
