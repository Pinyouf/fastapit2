import sys
import os
import pytest
# Adds the parent directory to the search path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.calculations import add, divide, multiply, subtract, BankAccount

@pytest.fixture
def zero_bank_account():
    return BankAccount()
@pytest.fixture
def bank_account_with_balance():
    return BankAccount(100)

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 5),
    (1, 1, 2),
    (0, 0, 0)
])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (5, 3, 2),
    (10, 5, 5),
    (0, 0, 0)
])
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (2, 3, 6),
    (1, 1, 1),
    (0, 0, 0)
])
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) == expected

@pytest.mark.parametrize("num1, num2, expected", [
    (6, 3, 2),
    (6, 0, 0)
])
def test_divide(num1, num2, expected):
    assert divide(num1, num2) == expected

def test_bank_set_initial_amount():
    bank_account = BankAccount(100)
    assert bank_account.balance == 100
    #assert zero_bank_account.balance == 0

def test_bank_default_initial_amount(zero_bank_account):
    #account = BankAccount()
    assert zero_bank_account.balance == 0

def test_withdraw(bank_account_with_balance):
    bank_account_with_balance.withdraw(30)
    assert bank_account_with_balance.balance == 70    
    with pytest.raises(ValueError):
        bank_account_with_balance.withdraw(100)

def test_deposit(bank_account_with_balance):
    bank_account_with_balance.deposit(50)
    assert bank_account_with_balance.balance == 150

def test_collect_interest(bank_account_with_balance):
    bank_account_with_balance.collect_interest()
    assert bank_account_with_balance.balance == 210

@pytest.mark.parametrize("deposited, withdrawn, expected", [
    (200, 100, 100),
    (50, 10, 40),
    (1200, 200, 1000)
])
def test_bank_transaction(zero_bank_account, deposited, withdrawn, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrawn)
    assert zero_bank_account.balance == expected

    