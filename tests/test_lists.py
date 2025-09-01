import pytest

from lists.exceptions import ListIsNotEmpty
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


def test_getitem_invalid(lists_path):
    lsm = ListsManager(lists_path, "raise")
    with pytest.raises(KeyError):
        lsm["fake.list"]


def test_get_invalid(lists_path):
    lsm = ListsManager(lists_path, "raise")
    assert lsm.get("fake.test") is None


def test_getitem_valid(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lm = lsm[list_path.name]
    assert lm.list_name == list_path.name


def test_get_valid(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lm = lsm.get(list_path.name)
    assert lm is not None
    assert lm.list_name == list_path.name


def test_create(lists_path):
    lsm = ListsManager(lists_path, "raise")
    lm = lsm.create("new.list", raise_if_exists=True)
    assert lm.list_name == "new.list"


def test_create_exists_raise(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    with pytest.raises(FileExistsError):
        lm = lsm.create(list_path.name, raise_if_exists=True)


def test_create_exists_ignore(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lm = lsm.create(list_path.name, raise_if_exists=False)
    assert lm.list_name == list_path.name


def test_remove_empty(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lsm.remove(list_path.name)


def test_remove_not_empty(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lm = lsm[list_path.name]
    lm.add("item1")
    with pytest.raises(ListIsNotEmpty):
        lsm.remove(list_path.name)


def test_remove_not_empty_force(lists_path, list_path):
    lsm = ListsManager(lists_path, "raise")
    lsm.remove(list_path.name, force=True)


def test_remove_non_exists_ignore(lists_path):
    lsm = ListsManager(lists_path, "raise")
    lsm.remove("fake.list", raise_if_not_exists=False)


def test_remove_non_exists_raise(lists_path):
    lsm = ListsManager(lists_path, "raise")
    with pytest.raises(FileNotFoundError):
        lsm.remove("fake.list", raise_if_not_exists=True)
