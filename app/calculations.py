def add(num1: int, num2: int) -> int:
    return num1 + num2

def subtract(num1: int, num2: int) -> int:
    return num1 - num2

def multiply(num1: int, num2: int) -> int:
    return num1 * num2

def divide(num1: int, num2: int) -> float:
    return num1 / num2 if num2 != 0 else 0


class BankAccount:
    def __init__(self, starting_balance=0):
        self.balance = starting_balance 

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
    def collect_interest(self):
        self.balance += self.balance * 1.1