from __future__ import annotations

import sys
from typing import Any

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias


JSONDict: TypeAlias = dict[str, Any]
"""Simple alias for type hinting `dict`s that can be passed to/from JSON-handling functions."""


class AuthenticationError(Exception):
    """Error raised on Spond authentication failure."""

    pass


def validate_list_of_data_dicts(data: list[JSONDict]) -> list[JSONDict]:
    """Return True if `data` is a list of data dicts.

    Raise TypeError with relevant message if not.
    """
    if not isinstance(data, list):
        err_msg = f"Expected a list, got {type(data)}: '{data}'."
        raise TypeError(err_msg)
    return [validate_data_dict(item) for item in data]


def validate_data_dict(data: JSONDict) -> JSONDict:
    """Return `data` if a dict with key `id`, i.e. looks like Spond data.

    Raise TypeError with relevant message if not.
    """
    if not isinstance(data, dict):
        err_msg = f"Expected a dict, got {type(data)}: '{data}'."
        raise TypeError(err_msg)
    if data.get("id"):
        return data
    err_msg = f"Expected key `id`; got keys '{data.keys}'."
    raise TypeError(err_msg)
