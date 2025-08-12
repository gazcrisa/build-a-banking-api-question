import pytest
from bank import InMemoryBank


def test_step1_basic_flow():
    bank = InMemoryBank()
    a = bank.create_account("Alice", 100)
    b = bank.create_account("Bob", 25)
    assert bank.get_balance(a) == 100
    assert bank.get_balance(b) == 25

    bank.deposit(a, 50)
    assert bank.get_balance(a) == 150

    bank.transfer(a, b, 20)
    assert bank.get_balance(a) == 130
    assert bank.get_balance(b) == 45


def test_step1_validation():
    bank = InMemoryBank()
    a = bank.create_account("Alice", 0)
    with pytest.raises(ValueError):
        bank.create_account("", 0)
    with pytest.raises(ValueError):
        bank.create_account("Bob", -1)
    with pytest.raises(ValueError):
        bank.deposit(a, -1)
    with pytest.raises(ValueError):
        bank.transfer(a, a, 1)
    with pytest.raises(ValueError):
        bank.transfer(a, 999, 1)
    with pytest.raises(ValueError):
        bank.transfer(999, a, 1)
    with pytest.raises(ValueError, match="insufficient funds"):
        bank.transfer(a, bank.create_account("Bob"), 10)


def test_step2_top_n_senders():
    bank = InMemoryBank()
    a = bank.create_account("Alice", 100)
    b = bank.create_account("Bob", 100)
    c = bank.create_account("Carol", 100)

    bank.transfer(a, b, 10)
    bank.transfer(a, c, 15)
    bank.transfer(b, c, 20)

    top1 = bank.top_n_senders(1)
    assert top1 == [(a, 25)], f"Expected Alice only, got {top1}"

    top2 = bank.top_n_senders(2)
    assert top2 == [(a, 25), (b, 20)], f"Expected Alice then Bob, got {top2}"

    top3 = bank.top_n_senders(3)
    assert top3 == [(a, 25), (b, 20)], "Carol has sent 0 and should be excluded"


def test_step2_ties_break_by_account_id():
    bank = InMemoryBank()
    a = bank.create_account("A", 100)
    b = bank.create_account("B", 100)
    c = bank.create_account("C", 100)

    bank.transfer(a, b, 10)
    bank.transfer(c, b, 10)

    result = bank.top_n_senders(5)
    assert result == sorted(result, key=lambda x: (-x[1], x[0]))
    assert result[0][1] == 10 and result[1][1] == 10
    assert result[0][0] < result[1][0], "Tie should break by ascending account_id"


def test_atomicity_on_insufficient_funds():
    bank = InMemoryBank()
    a = bank.create_account("Alice", 5)
    b = bank.create_account("Bob", 0)
    with pytest.raises(ValueError):
        bank.transfer(a, b, 10)
    # Balances unchanged
    assert bank.get_balance(a) == 5
    assert bank.get_balance(b) == 0
