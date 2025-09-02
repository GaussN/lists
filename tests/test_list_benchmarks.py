from random import randbytes
import sqlite3

import pytest
import pytest_benchmark

from lists.list_manager import ListManager


@pytest.fixture
def lm(lists_file) -> ListManager:
    """Return nonempty list manager."""
    with sqlite3.connect(lists_file) as conn:
        conn.execute("INSERT INTO lists(list_name) VALUES('list')")
        conn.execute("CREATE TABLE list ( item TEXT UNIQUE )")
        conn.commit()
    _lm = ListManager(lists_file, "list")
    for _ in range(500):
        _lm.add(randbytes(4).hex())
    yield _lm


def _setup_random_item():
    return (randbytes(4).hex(),), {}


@pytest.mark.benchmark(group="add")
def test_add_items_in_non_empty_list_benchmark(benchmark, lm):
    benchmark.pedantic(lm.add, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="has")
def test_has_items_benchmark(benchmark, lm):
    benchmark.pedantic(lm.has, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="remove")
def test_remove_items_benchmark(benchmark, lm):
    benchmark.pedantic(lm.remove, setup=_setup_random_item, rounds=1000)
