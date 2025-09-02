import logging
import os.path
import pathlib
import sqlite3

from typing import (
    Literal,
    LiteralString,
    Optional,
)

from lists.list_manager import ListManager
from lists.exceptions import (
    InvalidListname,
    ListAlreadyExists,
    ListIsNotEmpty,
    ListNotFound,
)


logger = logging.getLogger(__name__)


class ListsManager(object):
    """Manage the lists folder."""

    __meta_table = "__lists"
    __database_name = ".lists.db"

    def __init__(self, lists_path: str):
        """init.

        Args:
            lists_path(str) - folder where the lists are.

        Raises:
            FileNotFound - if List doesnt exists.
        """
        self.__lists_database = pathlib.Path(lists_path)
        if not self.__lists_database.exists():
            raise FileNotFoundError(self.__lists_database)
        self.__lists_database = self.__lists_database / self.__database_name
        with sqlite3.connect(self.__lists_database) as conn:
            conn.executescript(
                f"CREATE TABLE IF NOT EXISTS {self.__meta_table}( list_name TEXT UNIQUE )"
            )
            conn.commit()

    def __check_list_name(self, list_name: str) -> None:
        if list_name == self.__meta_table:
            raise InvalidListname(list_name, "reserved name")

    def __getitem__(self, list_name: LiteralString) -> ListManager:
        """Returns `ListManager` instance or
        raises `ListNotFound` exception if the list doesn't exists.
        """
        self.__check_list_name(list_name)
        return ListManager(self.__lists_database, list_name)  # raise ListNotFound

    def get(self, list_name: LiteralString) -> Optional[ListManager]:
        """Returns `ListManager` instance or None."""
        try:
            return self[list_name]
        except ListNotFound:
            return None

    def create(
        self, list_name: LiteralString, raise_if_exists: bool = False
    ) -> ListManager:
        """Create and return `ListManager` instance."""
        # breakpoint()
        self.__check_list_name(list_name)
        try:
            with sqlite3.connect(self.__lists_database) as conn:
                _ = conn.execute(
                    f"INSERT INTO {self.__meta_table}(list_name) VALUES(?)",
                    (list_name,),
                )
                cur = conn.execute(f"CREATE TABLE {list_name} ( item TEXT UNIQUE )")
                conn.commit()
            return ListManager(self.__lists_database, list_name)
        except sqlite3.IntegrityError:
            if raise_if_exists:
                raise ListAlreadyExists(list_name)
            logger.warning('create: list "%s" already exists', list_name)
            return ListManager(self.__lists_database, list_name)

    def remove(
        self, list_name: str, force: bool = False, raise_if_not_exists: bool = False
    ) -> None:
        """Remove list from db."""
        self.__check_list_name(list_name)
        with sqlite3.connect(self.__lists_database) as conn:
            try:
                if not force:
                    cur = conn.execute(f"SELECT COUNT(item) FROM {list_name}")
                    if cur.fetchone()[0] != 0:
                        raise ListIsNotEmpty(list_name)
                conn.execute(f"DROP TABLE {list_name}")
                conn.execute(
                    f"DELETE FROM {self.__meta_table} WHERE list_name = ?", (list_name,)
                )
                conn.commit()
            except sqlite3.OperationalError:
                if raise_if_not_exists:
                    raise ListNotFound(list_name)
                logger.warning('remove: list "%s" doesn\'t exists', list_name)
