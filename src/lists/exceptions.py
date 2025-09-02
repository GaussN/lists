class ListsError(Exception):
    pass


class ListAlreadyExists(ListsError):
    pass


class ListIsNotEmpty(ListsError):
    pass


class InvalidListname(ListsError):
    pass


class ListNotFound(ListsError):
    pass
