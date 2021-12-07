from typing import Optional

from client.model.user import User


class Account(User):
    def __init__(self, username: str, elo: int, account_id: Optional[int]):
        super().__init__(username=username)
        self.id = account_id
        self.elo = elo

    def set_account_id(self, account_id: int):
        self.id = account_id
