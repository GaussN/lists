# lists 

## Brief description
Local list database.

## Description
Interface to files with data in list view.

### Classes

#### ListsManager
##### Methods
`__init__(self, lists_path: str, name_normalize_policy: Literal)`
    
    params: 
        `lists_path` - forlder contains list files.
        `name_normalize_policy` - see [listname normalizer](#_listnamenormalizer)

`__getitem__(self, list_name: str) -> ListManager`

    params:
        `items` - list name.
    raises: 
        `KeyError` - if list with given name doesn't exists.
    returns:
        `ListManager` for given list.

`.get(self, item: str) -> Optional[ListManager]`

    Does the same as `__getitem__` but doesn't raise exception.
    Returns None if list doesn't exists instead.

`.create(self, list_name: str, raise_if_exists: bool = False) -> ListManager`

    Returns the created list or, if `raise_if_exists` is set to `False`, existing list, otherwise raises `FileExistsError`.

`.remove(self, list_name: str, force: bool = False, raise_if_not_exists: bool = False) -> None`

    raises:
        `ListIsNotEmpty` - if the list contains some content and `force` is set False.
        `FileNotFoundError` - if `raise_if_not_exists` is set True and list file doesn't exists.

#### ListManager
##### Methods
`.has(self, item: str) -> bool`  

`.add(self, item: str) -> bool`

    Returns `False` if the item is already in the list.

`.remove(self, item: str) -> bool`

    Returns `Fasle` if the item is not in the list.

##### Properties
`.list_path`

`.list_name`

#### _ListnameNormalizer
Check if list name contains characters or names prohibited by the OS 

For *nix: `/`, `\0` 

For Windows: `<` , `>` , `:` , `"` , `/` , `\` , `?` , `*` , `|` , `CON` , `PRN` , `AUX` , `NUL` , `COM[0-9]` , `LPT[0-9]`

##### Methods 
`.normalize(self, file_name: str) -> str`

    The method's action depends on the policy set in __init__
    
    Available policies:
    - `hide` - replaces all fobidden characteds with `_`.
    - `raise` - raises `InvalidListname(OSError)` exception.


## Example
Base usage
```python
from lists import ListsManager

user_id = ...
lists_manager = ListsManager("/var/lists/", name_normalize_policy="hide")
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
Nope