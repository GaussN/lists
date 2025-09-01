import sys

import pytest

from lists.exceptions import InvalidListname
from lists.normalizer import _ListnameNormalizer


filenames = (
    ("test\0.list", "test_.list"),
    ("test/.list", "test_.list"),
    (".", "_"),
    ("..", "_"),
)
if sys.platform == "win32":
    filenames = (
        ("test<.list", "test_.list"),
        ("test>.list", "test_.list"),
        ("test:.list", "test_.list"),
        ('test".list', "test_.list"),
        ("test/.list", "test_.list"),
        ("test\\.list", "test_.list"),
        ("test?.list", "test_.list"),
        ("test*.list", "test_.list"),
        ("test|.list", "test_.list"),
        ("CON", "_"),
        ("CON.list", "_"),
        ("PRN", "_"),
        ("PRN.list", "_"),
        ("AUX", "_"),
        ("AUX.list", "_"),
        ("NUL", "_"),
        ("NUL.list", "_"),
        *((f"COM{i}", "_") for i in range(1, 10)),
        *((f"COM{i}", "_") for i in range(1, 10)),
        *((f"LPT{i}.list", "_") for i in range(1, 10)),
        *((f"LPT{i}.list", "_") for i in range(1, 10)),
    )


@pytest.mark.parametrize("filename, normalized_filename", filenames)
def test_raise(filename: str, normalized_filename: str):
    fnn = _ListnameNormalizer(policy="raise")
    with pytest.raises(InvalidListname):
        fnn.normalize(filename)


@pytest.mark.parametrize("filename, normalized_filename", filenames)
def test_hide(filename: str, normalized_filename: str):
    fnn = _ListnameNormalizer(policy="hide")
    nf = fnn.normalize(filename)
    assert nf == normalized_filename


def test_normal():
    fnn = _ListnameNormalizer(policy="hide")
    assert "test.list" == fnn.normalize("test.list")
    assert "test" == fnn.normalize("test")
