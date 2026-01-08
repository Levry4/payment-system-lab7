"""
Value Objects - неизменяемые объекты доменной модели
"""

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class Money:
    """Value Object для денежных сумм"""
    amount: float
    currency: str = "USD"
    
    def __post_init__(self):
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        if not isinstance(self.amount, (int, float)):
            raise ValueError("Amount must be a number")
    
    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, Money):
            return False
        return self.amount == other.amount and self.currency == other.currency
    
    def __add__(self, other: 'Money') -> 'Money':
        if self.currency != other.currency:
            raise ValueError("Cannot add money with different currencies")
        return Money(self.amount + other.amount, self.currency)
    
    def __mul__(self, multiplier: float) -> 'Money':
        return Money(self.amount * multiplier, self.currency)
    
    def __str__(self) -> str:
        return f"{self.currency} {self.amount:.2f}"