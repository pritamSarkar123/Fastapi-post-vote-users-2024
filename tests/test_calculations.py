import pytest

from app.calculations import *


@pytest.fixture
def zero_bank_account():
    print("creating empty account")
    return BankAccount()


@pytest.fixture
def bank_account():
    print("creating account with balance of 50")
    return BankAccount(50)


# def test_add():
#     print("testing add function")
#     assert add(1, 2) == 3
#     assert add(0, 0) == 0
#     assert add(-1, 1) == 0
#     assert add(-1, -1) == -2
@pytest.mark.parametrize(
    "num1, num2, expected", [(0, 0, 0), (1, 2, 3), (-1, 1, 0), (-1, -1, -2)]
)
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected
    assert add(0, 0) == 0
    assert add(-1, 1) == 0
    assert add(-1, -1) == -2


def test_multiply():
    print("testing multiply function")
    assert multiply(1, 2) == 2
    assert multiply(0, 0) == 0
    assert multiply(-1, 1) == -1
    assert multiply(-1, -1) == 1


def test_divide():
    print("testing divide function")
    assert divide(1, 2) == 0.5
    # assert divide(0, 0) == 0
    assert divide(-1, 1) == -1
    assert divide(-1, -1) == 1

    with pytest.raises(ZeroDivisionError):
        divide(1, 0)

    with pytest.raises(ZeroDivisionError):
        divide(0, 0)


##########################################################################
def test_bank_set_initial_amount(
    bank_account,
):
    print("testing initial account balance start with 50")
    assert bank_account.balance == 50
    bank_account.deposit(100)
    assert bank_account.balance == 150


def test_bank_default_initial_amount(
    zero_bank_account,
):  # zero_bank_account is a variable contains the returen value of zero_bank_account fixture
    print("testing initial account balance start with 0")
    assert zero_bank_account.balance == 0
    zero_bank_account.deposit(100)
    assert zero_bank_account.balance == 100


def test_withdraw(bank_account):
    bank_account.withdraw(10)
    assert bank_account.balance == 40

    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(100)


def test_diposit(bank_account):
    bank_account.deposit(100)
    assert bank_account.balance == 150


def test_collect_interest(bank_account, zero_bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 5) == 55

    zero_bank_account = BankAccount()
    zero_bank_account.collect_interest()
    assert zero_bank_account.balance == 0


@pytest.mark.parametrize(
    "diposited, withdrew, expected",
    [(200, 100, 100), (50, 10, 40), (1200, 200, 1000), (0, 0, 0)],
)  # each time fixture will be called
def test_bank_transaction(zero_bank_account, diposited, withdrew, expected):
    zero_bank_account.deposit(diposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected


def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
