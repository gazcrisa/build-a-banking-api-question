# Technical Interview Exercise — Implement a Banking System

**Timebox:** ~60 minutes (plus 10–15 min discussion)  
**Language:** Python 3.11+

## Project layout

```
README.md
bank.py
requirements.txt
tests/
  └── test_bank.py
```

## Run tests

> Run these commands from the project root (where `bank.py` and `tests/` live).  
> Using `python -m pytest` ensures the venv’s Python is used.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m pytest -q
```

### Windows (PowerShell)

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m pytest -q
```

### Run only Step 1 tests

```bash
python -m pytest -q tests/test_bank.py::test_step1_basic_flow tests/test_bank.py::test_step1_validation tests/test_bank.py::test_atomicity_on_insufficient_funds
```

### Run only Step 2 tests

```bash
python -m pytest -q tests/test_bank.py::test_step2_top_n_senders tests/test_bank.py::test_step2_ties_break_by_account_id
```

### (Optional) Run a single test while iterating

```bash
python -m pytest -q tests/test_bank.py::test_step1_basic_flow
```

---

## Prompt

You're given an abstract base class `Bank` that defines a small banking interface. Implement `InMemoryBank` to satisfy the interface and the requirements below. Use in-memory data structures only — no databases.

### Step 1 — Core features

Implement the following behaviors (using **integers** for all balances and amounts; values must be **non-negative**):

1. `create_account(name: str, initial_balance: int = 0) -> int`

   - `name` must be a **non-empty string** (after trimming whitespace).
   - Creates a new account with a unique integer ID and a non-negative initial balance.
   - Returns the `account_id`.

2. `get_balance(account_id: int) -> int`

   - Returns the current balance.

3. `deposit(account_id: int, amount: int) -> None`

   - `amount` must be **positive**.
   - Increase the balance accordingly.

4. `transfer(src_account_id: int, dst_account_id: int, amount: int) -> None`
   - `amount` must be **positive**.
   - Disallow self-transfer (`src == dst`).
   - If `src` has insufficient funds, raise `ValueError("insufficient funds")`.
   - The operation must be atomic: on error, **no partial state** should be applied.
   - Record the transfer for Step 2 (see below).

### Step 2 — Analytics

5. `top_n_senders(n: int) -> list[tuple[int, int]]`
   - Return the top **n** account IDs by **total amount sent** via `transfer`.
   - Sort by total sent **descending**, breaking ties by **ascending account_id**.
   - Return a list of `(account_id, total_sent)` tuples.
   - Accounts with zero sent volume should not appear in the result.

---

## Constraints & Notes

- Integers only: no floating-point/Decimal.
- Validate inputs. For invalid IDs or parameters, raise `ValueError` with a clear message.
- Keep it single-threaded; but write code as if operations must stay consistent (simulate atomicity).
- Keep the public method signatures exactly as defined in `Bank`.
- You may add private helpers or internal types as needed.

### Bonus (if time permits)

- Add `get_statement(account_id)` returning a list of transaction entries (deposits and transfers in/out).
- Add `withdraw(account_id, amount)` following the same validation rules.
- Add idempotency support for `transfer` via an optional `txn_id: str` argument (ignore duplicate IDs).

## What we'll discuss afterwards

- Tradeoffs in data modeling (maps of balances, indexes for analytics).
- Error handling choices.
- Extensibility (e.g., fees, multi-currency, overdraw rules).
- Performance/scaling considerations and how you'd redesign for >10M accounts.
# build-a-banking-api-question
