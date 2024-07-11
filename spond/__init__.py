"""Top-level module. Contains typing alias and related functions."""

from typing import Any, Dict, Optional

from typing_extensions import TypeAlias

DictFromJSON: TypeAlias = Dict[str, Any]
"""Type annotation for functions that return API data."""


def is_list_of_dict(data: Optional[list]) -> bool:
    """Simple high-level type check for `list` of `dict`.

    Use when data from API call is expected to contain converted JSON array of
    elements. Does not check keys/values of `dict`.

    Returns
    -------
    True
        if `data` is `list[dict]`, otherwise False.

    """
    if data is None:
        return False  # handle None case separately for clarity
    if isinstance(data, list):
        if all(isinstance(item, dict) for item in data):
            return True
    return False
