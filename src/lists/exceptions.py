class ListsError(Exception):
    pass


class InvalidListname(ListsError):
    pass


class ListIsNotEmpty(ListsError):
    pass


class ListNotFound(ListsError):
    pass


class ListAlreadyExists(ListsError):
    pass
