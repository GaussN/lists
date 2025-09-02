import os.path
import pathlib
import sqlite3


class ListManager(object):
    """Basic operations with list."""

    def __init__(self, lists_path: str, list_name: str):
        self.__lists_path = lists_path
        with sqlite3.connect(self.__lists_path) as conn:
            cur = conn.execute("SELECT list_name FROM lists WHERE list_name = ?", (list_name,))
            fa = cur.fetchall()
            if fa.__len__() == 0:
                raise FileNotFoundError
        self.__list_name = list_name

    @property
    def list_name(self):
        return self.__list_name

    def __str__(self):
        return f"{self.__class__.__name__}({self.list_name})"

    def has(self, item: str) -> bool:
        """Is item in the list."""
        with sqlite3.connect(self.__lists_path) as conn:
            cur = conn.execute(f"SELECT item FROM {self.__list_name} WHERE item = ?", (item,))
            return cur.fetchall()

    def remove(self, item: str) -> bool:
        """Remove item from the list.

        Returns:
            bool: True if the item removed,
                    if the item is not in the list - False
        """
        with sqlite3.connect(self.__lists_path) as conn:
            cur = conn.execute(f"DELETE FROM {self.__list_name} WHERE item = ?", (item,))
            fa = cur.fetchall()
            conn.commit()
            return not not cur.rowcount


    def add(self, item: str) -> bool:
        """Adds item to the list if it is not in it.

        Returns:
            bool: True if the item was added,
                    if the item was already in the list - False.
        """
        with sqlite3.connect(self.__lists_path) as conn:
            try:
                cur = conn.execute(f"INSERT INTO {self.__list_name}(item) VALUES(?)", (item,))
                conn.commit()
            except sqlite3.IntegrityError:
                return False
            return True
