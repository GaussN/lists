import logging
import os.path
import pathlib

from typing import (
    Literal,
    Optional,
)

from lists.normalizer import _ListnameNormalizer
from lists.list_manager import ListManager
from lists.exceptions import ListIsNotEmpty


logger = logging.getLogger(__name__)


class ListsManager(object):
    """Manage the lists folder."""

    def __init__(
        self, lists_path: str, name_normalize_policy: Literal["raise", "hide"] = "raise"
    ):
        """init.

        Args:
            lists_path(str) - folder where the lists are.
            name_normalize_police(str) - see _ListnameNormalizer.

        Raises:
            FileNotFound - if List doesnt exists.
            ValueError - if `name_noralize_policy` is incorrect.
        """
        self.__lists_path = pathlib.Path(lists_path)
        if not self.__lists_path.exists():
            raise FileNotFoundError(self.__lists_path)
        self.__normalizer = _ListnameNormalizer(policy=name_normalize_policy)

    def __getitem__(self, list_name: str) -> ListManager:
        """Returns `ListManager` instance or
        raises `KeyError` exception if the list doesn't exists.
        """
        list_name = self.__normalizer.normalize(list_name)
        list_path = os.path.join(self.__lists_path, list_name)
        if not os.path.exists(list_path):
            raise KeyError(list_path)
        return ListManager(list_path)

    def get(self, list_name: str) -> Optional[ListManager]:
        """Returns `ListManager` instance or None."""
        list_name = self.__normalizer.normalize(list_name)
        list_path = self.__lists_path / list_name
        if os.path.exists(list_path):
            return ListManager(list_path)
        return None

    def create(self, list_name: str, raise_if_exists: bool = False) -> ListManager:
        """Create and return `ListManager` instance."""
        list_name = self.__normalizer.normalize(list_name)
        lm = self.get(list_name)
        if lm is None:
            with (self.__lists_path / list_name).open("w"):
                pass
            return ListManager(self.__lists_path / list_name)
        if raise_if_exists:
            raise FileExistsError(list_name)
        import warnings

        logger.warning('create: list "%s" already exists', list_name)
        return lm

    def remove(
        self, list_name: str, force: bool = False, raise_if_not_exists: bool = False
    ) -> None:
        """Remove list file."""
        list_name = self.__normalizer.normalize(list_name)
        list_path = self.__lists_path / list_name
        try:
            if not force:
                size = os.path.getsize(list_path)
                if size != 0:
                    raise ListIsNotEmpty(list_name)
            os.remove(list_path)
        except FileNotFoundError:
            if raise_if_not_exists:
                raise
            logger.warning('remove: list "%s" doesn\'t exists', list_name)
