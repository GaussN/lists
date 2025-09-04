import os.path
import pathlib

from lists.exceptions import ListNotFound


class ListManager(object):
    """Basic operations with list."""

    def __init__(self, list_path: str):
        if not os.path.exists(list_path):
            raise ListNotFound(list_path)
        self.__list_path = list_path
        self.__list_name = str(self.__list_path).split(os.path.sep)[-1]

    @property
    def list_path(self):
        return self.__list_path

    @property
    def list_name(self):
        return self.__list_name

    def __str__(self):
        return f"{self.__class__.__name__}({self.__lists_path.split(os.path.sep)[-1]})"

    def __has(self, item: str) -> int:
        item += "\n"
        i = 1
        with open(self.__list_path, "r") as file:
            char = file.read(1)
            j = 0
            while char and j < len(item) - 1:
                if item[j] == char:
                    char = file.read(1)
                    i += 1
                    j += 1
                    continue 
                j = 0
                while char and char != "\n":
                    char = file.read(1)
                    i += 1
                char = file.read(1)
                i += 1
            # pattern = item + \n
            # so pattern position is i(end of comparing) - len(item+\n) - 1
            #                                           or len(item)
            return i - len(item) if j == len(item) - 1 else -1

    def has(self, item: str) -> bool:
        """Is item in the list."""
        return self.__has(item) != -1

    def remove(self, item: str) -> bool:
        """Remove item from the list.

        Returns:
            bool: True if the item removed,
                    if the item is not in the list - False
        """
        pos = self.__has(item)
        if pos == -1:
            return False
        with open(self.__list_path, "rt+") as file:
            file.seek(pos)
            file.truncate(len(item) + 1)
        return True

    def add(self, item: str) -> bool:
        """Adds item to the list if it is not in it.

        Returns:
            bool: True if the item was added,
                    if the item was already in the list - False.
        """
        if self.has(item):
            return False
        with open(self.__list_path, "at") as file:
            file.write(item + "\n")
        return True
