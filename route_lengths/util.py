from typing import List, Dict, Union, Callable, Any


def index_by(
    items: List[Any],
    key_getter: Union[str, Callable[[Any], str]],
) -> Dict[str, Any]:
    res = {}
    if isinstance(key_getter, str):
        key_getter_as_str = key_getter
        key_getter = lambda dict: dict[key_getter_as_str]
    for item in items:
        key = key_getter(item)
        res[key] = item
    return res


def bucket_by(
    items: List[Any],
    key_getter: Union[str, Callable[[Any], str]],
) -> Dict[str, List[Any]]:
    res = {}
    if isinstance(key_getter, str):
        key_getter_as_str = key_getter
        key_getter = lambda dict: dict[key_getter_as_str]
    for item in items:
        key = key_getter(item)
        res.setdefault(key, [])
        res[key].append(item)
    return res


def pairwise(some_list: List[Any]):
    for index in range(len(some_list) - 1):
        yield some_list[index], some_list[index + 1]
