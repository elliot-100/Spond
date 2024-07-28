
from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from .base import _SpondBase

if TYPE_CHECKING:
    # from datetime import datetime

    from . import DictFromJSON


class Chat(_SpondBase):

    # DT_FORMAT = "%Y-%m-%dT00:00:00.000Z"

    def __init__(self, username: str, password: str) -> None:
        super().__init__(username, password, "https://api.spond.com/core/v1/")
        self.chats = None
        self.messages = None


    async def login(self) -> None:
        login_url = f"{self.api_url}login"
        data = {"email": self.username, "password": self.password}
        async with self.clientsession.post(login_url, json=data) as r:
            login_result = await r.json()
            self.token = login_result.get("loginToken")
            if self.token is None:
                err_msg = f"Login failed. Response received: {login_result}"
                raise AuthenticationError(err_msg)

    @_SpondBase.require_authentication
    async def get_messages(
        self,
        maximum: int = 100,
    ) -> Optional[DictFromJSON]:
        """
        Retrieve messages.

        Parameters
        ----------
        maximum : int, optional
            Set a limit on the number of messages returned.
            For performance reasons, defaults to 100.
            Uses `max` API parameter, but that's a Python built-in function.

        Returns
        -------
        list[dict] or None
            A list of messages, each represented as a dictionary, or None if no
            messages are available.
        """
        url = f"https://api.spond.com/chat/v1/chats"
        async with self.clientsession.get(
            url,
            headers=self.auth_headers,
            params={"max": str(maximum)},
        ) as r:
            self.messages = await r.json()
        return self.messages

