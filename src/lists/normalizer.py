import sys
import re
from functools import wraps
from typing import (
    Literal,
)

from lists.exceptions import InvalidListname


class _ListnameNormalizer(object):
    """Check if file name contains forbbiden characters.

    There are two strategies:
        raise - throw `InvalidListname` if string contains forbidden chars.
        hide - set foebbiden chars to `_`.
    """

    if sys.platform == "win32":
        __incorrect = re.compile(
            r"([<>:\"/\?*|])|(^((CON)|(PRN)|(AUX)|(NUL)|(COM[0-9])|(LPT[0-9]))(\..*)?$)"
        )
    else:
        __incorrect = re.compile(r"([/\x00])|(^\.{1,2}$)")

    def __init__(self, *, policy: Literal["raise", "hide"]):
        self.__policy = policy
        _normalize_method = {
            "raise": self.__normalize_raise,
            "hide": self.__normalize_hide,
        }.get(self.__policy)
        if _normalize_method is None:
            raise ValueError(policy, "Invalid policy value")

        @wraps(_normalize_method)
        def wrapper(*args, **kwargs):
            return _normalize_method(*args, **kwargs)

        self.normalize = wrapper

    def __normalize_raise(self, file_name: str) -> str:
        """Raise InvalidFilename exception if `file_name` is incorrect."""
        if m := self.__incorrect.findall(file_name):
            raise InvalidListname(file_name, m)
        return file_name

    def __normalize_hide(self, file_name: str) -> str:
        """Hide(replace with underscope) all incorrect characters in `file_name`."""
        file_name = self.__incorrect.sub("_", file_name)
        return file_name
