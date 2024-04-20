from .base import SpondBase
import aiohttp


class SpondClub(SpondBase):
    def __init__(self, username, password):
        super().__init__(username, password, "https://api.spond.com/club/v1/")
        self.transactions = None

    @SpondBase.require_authentication
    async def get_transactions(
        self, club_id: str, skip: int = None, max_items: int = 100
    ):
        """Get transactions / payments made

        Args:
            club_id (str): This Club ID is different than the Group ID from core API.
            max_items (int, optional): Max transactions to grab. Defaults to 100.
            skip (int, optional): This endpoint only returns 25 transactions at a time
                (page scrolling). Therefore, we need to increment this `skip` param to
                grab the next 25 etc. Defaults to None. It's better if users keep `skip`
                at None and specify `max_items` instead. This param is only here for the
                recursion implementation

        Returns:
            list[dict]: each payment as a json dict
        """
        if self.transactions is None:
            self.transactions = list()

        url = f"{self.api_url}transactions"
        params = None if skip is None else {"skip": skip}
        headers = {**self.auth_headers, "X-Spond-Clubid": club_id}

        async with aiohttp.ClientSession() as session:
            async with session.get(url, headers=headers, params=params) as response:
                if response.status == 200:
                    t = await response.json()
                    if len(t) == 0:
                        return self.transactions

                    self.transactions.extend(t)
                    if len(self.transactions) < max_items:
                        return await self.get_transactions(
                            club_id=club_id,
                            skip=len(t) if skip is None else skip + len(t),
                            max_items=max_items,
                        )

        return self.transactions
