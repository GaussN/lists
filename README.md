# lists (sqlite)

## Brief description
Local list database.

## Description
Interface for storing named lists in sqlite

### Classes

#### ListsManager
##### Methods
`__init__(self, lists_path: str)`
    
    params: 
        `lists_path` - forlder contains list files.
    raises:
        `FileNotFoundError`.

`__getitem__(self, list_name: LiteralString) -> ListManager`

    raises: 
        `ListNotFound`.

`.get(self, list_name: LiteralString) -> Optional[ListManager]`

    Does the same as `__getitem__` but doesn't raise exception.
    Returns None if list doesn't exists instead.

`.create(self, list_name: LiteralString, raise_if_exists: bool = False) -> ListManager`

    Returns the created list or, if `raise_if_exists` is set to `False`, existing list, otherwise raises `ListAlreadyExists`.

`.remove(self, list_name: LiteralString, force: bool = False, raise_if_not_exists: bool = False) -> None`

    raises:
        `ListIsNotEmpty` - if the list contains some content and `force` is set False.
        `ListNotFound` - if `raise_if_not_exists` is set True and list file doesn't exists.

##### Raises
`InvalidListname`

    Can be raised in any method if `list_name` is equals to the `__meta_table` variable(`__lists` by default).


#### ListManager
##### Methods
`.has(self, item: str) -> bool`  

`.add(self, item: str) -> bool`

    Returns `False` if the item is already in the list.

`.remove(self, item: str) -> bool`

    Returns `Fasle` if the item is not in the list.

##### Properties
`.list_name`


## Example
Base usage
```python
from lists import ListsManager

user_id = ...
lists_manager = ListsManager("/var/lists/")
black_list = lists_manager.get("black_list")
if black_list is None:
    black_list = lists_manager.create("black_list")

if black_list.has(user_id):
    print("user banned.")
else:
    print("user not banned")
```

## Testing
### Tests
`uv run pytest`

### Benchark
`uv run pytest --benchmark-only --benchmark-warmup=true`

## Changelog
- The backend has been rewritten from files to sqlite.
    - speed has increased.
    - size of the list files also has increased :smiling_face_with_tear:.