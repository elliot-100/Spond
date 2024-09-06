"""Unofficial Python SDK for the Spond API.

The main entry point is `spond.spond.Spond` for general account/event/group/
messaging access, and `spond.club.SpondClub` for the Spond Club finance API.
"""

from typing import Any, TypeAlias

JSONDict: TypeAlias = dict[str, Any]
"""Simple alias for type hinting `dict`s that can be passed to/from JSON-handling functions."""


class AuthenticationError(Exception):
    """Raised when login to the Spond API fails.

    Typical causes:

    - Incorrect username/password.
    - 2FA enabled on the account (the library does not currently support
      Spond's TOTP flow).
    - The account has hit Spond's login rate limit (`outOfLoginAttempts`).
    - The Spond login API has changed shape and the response no longer
      contains an `accessToken`.

    The exception message includes any of the response's whitelisted
    diagnostic fields (`error`, `errorKey`, `errorCode`, `message`) so
    most error cases are self-explanatory. Other response fields — such
    as 2FA challenge tokens and (masked) `phoneNumber` — are intentionally
    dropped from the message to avoid leaking them into application logs.
    """

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
