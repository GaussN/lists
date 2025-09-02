from random import randbytes

import pytest
import pytest_benchmark

from lists.list_manager import ListManager


@pytest.fixture
def lm(list_path) -> ListManager:
    """Return nonempty list manager."""
    _lm = ListManager(list_path)
    for _ in range(500):
        _lm.add(randbytes(4).hex())
    yield _lm


def _setup_random_item():
    return (randbytes(4).hex(),), {}


@pytest.mark.benchmark(group="add")
def test_add_items_in_empty_list_benchmark(benchmark, list_path):
    lm = ListManager(list_path)
    benchmark.pedantic(lm.add, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="add")
def test_add_items_in_non_empty_list_benchmark(benchmark, lm):
    benchmark.pedantic(lm.add, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="has")
def test_has_items_benchmark(benchmark, lm):
    benchmark.pedantic(lm.has, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="remove")
def test_remove_items_benchmark(benchmark, lm):
    benchmark.pedantic(lm.remove, setup=_setup_random_item, rounds=1000)
