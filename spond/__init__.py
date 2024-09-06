from __future__ import annotations

import sys
from typing import Any, Dict

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias


JSONDict: TypeAlias = Dict[str, Any]
"""Simple alias for type hinting `dict`s that can be passed to/from JSON-handling functions."""


def is_list_spond_data_dict(data: list[JSONDict]) -> bool:
    """Return True if data is EITHER a list of data dicts, with `id` keys, OR is None.

    Raise TypeError with relevant message if not.
    """
    if data is None:
        return True
    if not isinstance(data, list):
        err_msg = f"Expected a list, got {type(data)}: '{data}'."
        raise TypeError(err_msg)
    return all(is_spond_data_dict(item) for item in data)


def is_spond_data_dict(data: JSONDict) -> bool:
    """Return True if data is a data dict with key `id`.

    Raise TypeError with relevant message if not.
    """
    if not isinstance(data, dict):
        err_msg = f"Expected a dict, got {type(data)}: '{data}'."
        raise TypeError(err_msg)
    if data.get("id"):
        return True
    err_msg = f"Expected key `id`; got keys '{data.keys}'."
    raise TypeError(err_msg)



