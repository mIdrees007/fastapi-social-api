
import pytest

from app.calculations import add, multiply, subtract, divide, BankAccount, InsufficientFunds

@pytest.fixture
def zero_bank_account():
    print("creating empty bank account")
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)
@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (3, 2, 5),
        (7, 1, 8),
        (12, 4, 16),
    ]
)
def test_add(num1, num2, expected):
    print("testing add function")
    assert add(num1, num2) == expected


@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (3, 2, 1),
        (7, 1, 6),
        (12, 4, 8),
    ]
)
def test_subtract(num1, num2, expected):
    assert subtract(num1, num2) == expected


@pytest.mark.parametrize(
    "num1, num2, expected",
    [
        (3, 2, 6),
        (7, 1, 7),
        (12, 4, 48),
    ]
)
def test_multiply(num1, num2, expected):
    assert multiply(num1, num2) == expected


def test_bank_set_initial_amount(bank_account):
   

    assert bank_account.balance == 50

def test_bank_default_amount(zero_bank_account):
    print("default amount")
    assert zero_bank_account.balance == 0
    
def test_withdraw(bank_account):
  
    assert bank_account.withdraw(20) == 30
def test_depoist(bank_account):
    
    assert bank_account.withdraw(20) == 30
    
def test_collect_interest(bank_account):
    
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 55
    
@pytest.mark.parametrize(
    "deposited, withdraw, expected",
    [
        (200, 100, 100),
        (50, 10, 40),
        (100, 50, 50),
    ]
)
def test_bank_transaction(zero_bank_account, deposited, withdraw, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdraw)
    assert zero_bank_account.balance == expected   
    
    
def test_insufficient_funds(bank_account):
    with pytest.raises(InsufficientFunds):
        bank_account.withdraw(200)
        
