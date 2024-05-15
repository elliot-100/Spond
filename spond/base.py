import aiohttp


class AuthenticationError(Exception):
    pass


class SpondBase:
    def __init__(self, username, password, api_url):
        self.username = username
        self.password = password
        self.api_url = api_url
        self.clientsession = aiohttp.ClientSession(cookie_jar=aiohttp.CookieJar())
        self.token = None

    @property
    def auth_headers(self):
        return {
            "content-type": "application/json",
            "Authorization": f"Bearer {self.token}",
        }

    def require_authentication(func: callable):
        async def wrapper(self, *args, **kwargs):
            if not self.token:
                try:
                    await self.login()
                except AuthenticationError as e:
                    await self.clientsession.close()
                    raise e
            return await func(self, *args, **kwargs)

        return wrapper

    async def login(self):
        login_url = f"{self.api_url}login"
        data = {"email": self.username, "password": self.password}
        async with self.clientsession.post(login_url, json=data) as r:
            login_result = await r.json()
            self.token = login_result.get("loginToken")
            if self.token is None:
                err_msg = f"Login failed. Response received: {login_result}"
                raise AuthenticationError(err_msg)
