import logging
import os.path
import pathlib
import sqlite3
import warnings

from typing import (
    Literal,
    Optional,
)

from lists.normalizer import _ListnameNormalizer
from lists.list_manager import ListManager
from lists.exceptions import ListIsNotEmpty, InvalidListname


logger = logging.getLogger(__name__)


class ListsManager(object):
    """Manage the lists folder."""

    def __init__(
        self, lists_path: str, name_normalize_policy: Literal["raise", "hide"] = None
    ):
        """init.

        Args:
            lists_path(str) - folder where the lists are.
            name_normalize_police(str) - see _ListnameNormalizer.

        Raises:
            FileNotFound - if List doesnt exists.
            ValueError - if `name_noralize_policy` is incorrect.
        """
        if name_normalize_policy is not None:
            warnings.deprecated("name_normalize_policy is deprecated parameter.")
        self.__lists_path = pathlib.Path(lists_path)
        if not self.__lists_path.exists():
            raise FileNotFoundError(self.__lists_path)
        self.__lists_path = self.__lists_path / ".lists.db"
        with sqlite3.connect(self.__lists_path) as conn:
            conn.executescript("CREATE TABLE IF NOT EXISTS lists( list_name TEXT UNIQUE )")
            conn.commit()
        # self.__normalizer = _ListnameNormalizer(policy=name_normalize_policy)

    def __getitem__(self, list_name: str) -> ListManager:
        """Returns `ListManager` instance or
        raises `KeyError` exception if the list doesn't exists.
        """
        if list_name == "lists":
            raise InvalidListname(list_name)
        with sqlite3.connect(self.__lists_path) as conn:
            
            cur = conn.execute("SELECT list_name FROM lists WHERE list_name = ?", (list_name,))
            if not cur.fetchall():
                raise KeyError
        return ListManager(self.__lists_path, list_name)

    def get(self, list_name: str) -> Optional[ListManager]:
        """Returns `ListManager` instance or None."""
        try:
            return self[list_name]
        except KeyError:
            return None

    def create(self, list_name: str, raise_if_exists: bool = False) -> ListManager:
        """Create and return `ListManager` instance."""
        lm = self.get(list_name)
        if lm is None:
            with sqlite3.connect(self.__lists_path) as conn:
                _ = conn.execute("INSERT INTO lists(list_name) VALUES(?)", (list_name,))
                cur = conn.execute(f"CREATE TABLE {list_name} ( item TEXT UNIQUE )")
                conn.commit()
            return ListManager(self.__lists_path, list_name)
        if raise_if_exists:
            raise FileExistsError(list_name)
        logger.warning('create: list "%s" already exists', list_name)
        return lm

    def remove(
        self, list_name: str, force: bool = False, raise_if_not_exists: bool = False
    ) -> None:
        """Remove list file."""
        lm = self.get(list_name)
        if lm is None:
            if raise_if_not_exists:
                raise FileNotFoundError
            logger.warning('remove: list "%s" doesn\'t exists', list_name)
            return 

        with sqlite3.connect(self.__lists_path) as conn:
            if not force:
                cur = conn.execute(f"SELECT COUNT(item) FROM {list_name}")
                # breakpoint()
                if cur.fetchone()[0] != 0:
                    raise ListIsNotEmpty(list_name)
            conn.execute(f"DELETE FROM {list_name}")
            conn.execute(f"DROP TABLE {list_name}")
            conn.execute("DELETE FROM lists WHERE list_name = ?", (list_name,))
            conn.commit()
