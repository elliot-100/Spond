import sys
from typing import Any, Dict

if sys.version_info < (3, 10):
    from typing_extensions import TypeAlias
else:
    from typing import TypeAlias


JSONDict: TypeAlias = Dict[str, Any]
"""Simple alias for type hinting `dict`s that can be passed to/from JSON-handling functions."""


def is_list_of_dicts(value: list[JSONDict]) -> bool:
    """Return True if `value` is a list of dicts, OR is None.

    Raise TypeError with relevant message if not.
    """
    if value is None:
        return True
    if not isinstance(value, list) or not all(isinstance(item, dict) for item in value):
        err_msg = f"Expected a list of dicts; got {type(value)}: '{value}'."
        raise TypeError(err_msg)
