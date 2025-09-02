import pytest

from lists.exceptions import ListIsNotEmpty
from lists.lists_manager import ListsManager


@pytest.mark.skip("deprecated")
def test_incorrect_police(lists_path):
    with pytest.raises(ValueError):
        ListsManager(lists_path, "uncorrect_policy")


@pytest.mark.skip("deprecated")
@pytest.mark.parametrize("policy", ("raise", "hide"))
def test_correct_policy(lists_path, policy):
    ListsManager(lists_path, policy)


def test_incorrect_path():
    with pytest.raises(FileNotFoundError):
        ListsManager("fake_path")


def test_getitem_invalid(lists_path):
    lsm = ListsManager(lists_path)
    with pytest.raises(KeyError):
        lsm["fake_list"]


def test_get_invalid(lists_path):
    lsm = ListsManager(lists_path)
    assert lsm.get("fake_list") is None


def test_getitem_valid(lists_path):
    lsm = ListsManager(lists_path, "raise")
    lsm.create("list")
    lm = lsm["list"]
    assert lm.list_name == "list"


def test_get_valid(lists_path):
    lsm = ListsManager(lists_path)
    lsm.create("list")
    lm = lsm.get("list")
    assert lm is not None
    assert lm.list_name == "list"


def test_create(lists_path):
    lsm = ListsManager(lists_path)
    lm = lsm.create("list", raise_if_exists=True)
    assert lm.list_name == "list"


def test_create_exists_raise(lists_path):
    lsm = ListsManager(lists_path)
    lsm.create("list", raise_if_exists=True)
    with pytest.raises(FileExistsError):
        lm = lsm.create("list", raise_if_exists=True)


def test_create_exists_ignore(lists_path):
    lsm = ListsManager(lists_path)
    lsm.create("list", raise_if_exists=False)
    lm = lsm.create("list", raise_if_exists=False)
    assert lm.list_name == "list"


def test_remove_empty(lists_path):
    lsm = ListsManager(lists_path, "raise")
    lsm.create("list", raise_if_exists=False)
    lsm.remove("list")


def test_remove_not_empty(lists_path):
    lsm = ListsManager(lists_path)
    lm = lsm.create("list", raise_if_exists=False)
    lm.add("item1")
    with pytest.raises(ListIsNotEmpty):
        lsm.remove("list")


def test_remove_not_empty_force(lists_path):
    lsm = ListsManager(lists_path)
    lm = lsm.create("list")
    lm.add("item1")
    lsm.remove("list", force=True)


def test_remove_non_exists_ignore(lists_path):
    lsm = ListsManager(lists_path)
    lsm.remove("fake_list", raise_if_not_exists=False)


def test_remove_non_exists_raise(lists_path):
    lsm = ListsManager(lists_path)
    with pytest.raises(FileNotFoundError):
        lsm.remove("fake_list", raise_if_not_exists=True)
