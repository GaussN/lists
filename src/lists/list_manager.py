import os.path
import pathlib


def _kmp_prefix(string: str) -> list:
    mask = [0] * len(string)
    ci = 0
    for i in range(1, len(string)):
        while ci > 0 and string[ci] != string[i]:
            ci = mask[ci - 1]
        if string[ci] == string[i]:
            ci += 1
        mask[i] = ci
    return mask


class ListManager(object):
    """Basic operations with list."""

    def __init__(self, list_path: str):
        if not os.path.exists(list_path):
            raise FileNotFoundError(list_path)
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

    def has(self, item: str) -> bool:
        """Is item in the list."""
        item += "\n"
        item_prefix = _kmp_prefix(item)
        with open(self.__list_path, "r") as file:
            char = file.read(1)
            j = 0
            while char and j < len(item) - 1:
                while j > 0 and char != item[j]:
                    j = item_prefix[j - 1]
                if char == item[j]:
                    j += 1
                char = file.read(1)
        return j == len(item) - 1

    def remove(self, item: str) -> bool:
        """Remove item from the list.

        Returns:
            bool: True if the item removed,
                    if the item is not in the list - False
        """
        # TODO : dont rewrite file
        items: set
        with open(self.__list_path, "rt") as file:
            items = set(file.readlines())
        try:
            items.remove(item + "\n")
        except KeyError:
            return False
        with open(self.__list_path, "wt") as file:
            file.writelines(items)
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
