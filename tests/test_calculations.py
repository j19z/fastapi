from app.calculations import add, substract, BankAccount, InsuficientFunds
import pytest

@pytest.fixture
def zero_bank_account():
    print ('creating an empty bank account')
    return BankAccount()

@pytest.fixture
def bank_account():
    return BankAccount(50)



@pytest.mark.parametrize('num1, num2, expected',[
                         (3,2,5),
                         (5,5,10),
                         (90,10,100)]) # note the quotes one in the staet and one in the end
def test_add(num1,num2, expected):
    print('Testing add function:')  
    assert add(num1, num2) == expected
    
def test_substract(): 
    assert substract(5, 3) == 2
    

# these two tests are running with fixtures
def test_bank_set_initial_amount(bank_account):
    assert bank_account.balance == 50
    
def test_bank_default_amount(zero_bank_account):
    print('testing my bank account')
    assert zero_bank_account.balance == 0
    
def test_withdraw():
    bank_account = BankAccount(50)
    bank_account.withdraw(10)
    assert bank_account.balance == 40
    
def test_deposit():
    bank_account = BankAccount(50)
    bank_account.deposit(10)
    assert bank_account.balance == 60
    
def test_interest():
    bank_account = BankAccount(100)
    bank_account.collect_interest()
    assert round(bank_account.balance, 6) == 110


# This function uses fixtures and "mark.parametrize" 
@pytest.mark.parametrize('deposited, withdrew1, withdrew2, expected',[
                         (10,2,2,6),
                         (100,5,10, 85),
                         (90,10,80,0)]) 
def test_bank_transaction(zero_bank_account, deposited, withdrew1, withdrew2, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew1)
    zero_bank_account.withdraw(withdrew2)
    assert zero_bank_account.balance == expected 

# This function tests exceptions  
def test_insuffienct_funds(bank_account):
    with pytest.raises(InsuficientFunds):
        bank_account.withdraw(200)
    