from random import randbytes

import pytest
import pytest_benchmark

from lists.list_manager import ListManager


@pytest.fixture
def lm(list_manager) -> ListManager:
    """Return nonempty list manager."""
    for _ in range(500):
        list_manager.add(randbytes(4).hex())
    yield list_manager


def _setup_random_item():
    return (randbytes(4).hex(),), {}


@pytest.mark.benchmark(group="add")
def test_add_benchmark(benchmark, lm):
    benchmark.pedantic(lm.add, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="has")
def test_has_benchmark(benchmark, lm):
    benchmark.pedantic(lm.has, setup=_setup_random_item, rounds=1000)


@pytest.mark.benchmark(group="remove")
def test_remove_benchmark(benchmark, lm):
    benchmark.pedantic(lm.remove, setup=_setup_random_item, rounds=1000)
