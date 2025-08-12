from __future__ import annotations
from abc import ABC, abstractmethod


class Bank(ABC):
    @abstractmethod
    def create_account(self, name: str, initial_balance: int = 0) -> int: ...
    @abstractmethod
    def get_balance(self, account_id: int) -> int: ...
    @abstractmethod
    def deposit(self, account_id: int, amount: int) -> None: ...
    @abstractmethod
    def transfer(self, src_account_id: int, dst_account_id: int, amount: int) -> None: ...
    @abstractmethod
    def top_n_senders(self, n: int) -> list[tuple[int, int]]: ...


# ---- Candidate implements this ----
class InMemoryBank(Bank):
    def __init__(self) -> None:
        pass

    def create_account(self, name: str, initial_balance: int = 0) -> int:
        raise NotImplementedError

    def get_balance(self, account_id: int) -> int:
        raise NotImplementedError

    def deposit(self, account_id: int, amount: int) -> None:
        raise NotImplementedError

    def transfer(self, src_account_id: int, dst_account_id: int, amount: int) -> None:
        raise NotImplementedError

    def top_n_senders(self, n: int) -> list[tuple[int, int]]:
        raise NotImplementedError


if __name__ == "__main__":
    bank = InMemoryBank()
