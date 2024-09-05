from __future__ import annotations

from abc import ABC
from collections.abc import Awaitable
from typing import Callable, Self, Any

import aiohttp

from spond import AuthenticationError


class _SpondBase(ABC):
    def __init__(self, username: str, password: str, api_url: str) -> None:
        self.username = username
        self.password = password
        self.api_url = api_url
        self.clientsession = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
        self.token = None

    @property
    def auth_headers(self) -> dict[str, str]:
        return {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    @staticmethod
    def require_authentication(func: Callable) -> Callable:
        async def wrapper(self: Self, *args: Any, **kwargs: Any) -> Awaitable:
            if not self.token:
                await self.login()
            return await func(self, *args, **kwargs)

        return wrapper

    async def login(self) -> None:
        login_url = f"{self.api_url}login"
        data = {"email": self.username, "password": self.password}
        async with self.clientsession.post(login_url, json=data) as r:
            login_result = await r.json()
            self.token = login_result.get("loginToken")
            if self.token is None:
                err_msg = f"Login failed. Response received: {login_result}"
                raise AuthenticationError(err_msg)
