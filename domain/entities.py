"""
Доменные сущности и бизнес-правила
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional
from enum import Enum
from .value_objects import Money


class OrderStatus(Enum):
    """Статусы заказа"""
    CREATED = "created"
    PAID = "paid"
    CANCELLED = "cancelled"


@dataclass
class OrderLine:
    """Строка заказа - часть агрегата Order"""
    product_name: str
    quantity: int
    unit_price: Money
    
    @property
    def total(self) -> Money:
        """Итоговая сумма для строки заказа"""
        return self.unit_price * self.quantity


class Order:
    """Агрегат Заказ - корневая сущность"""
    
    def __init__(self, order_id: str, customer_id: str, lines: List[OrderLine] = None):
        self.order_id = order_id
        self.customer_id = customer_id
        self._lines: List[OrderLine] = lines or []
        self.status: OrderStatus = OrderStatus.CREATED
        self.created_at: datetime = datetime.now()
        self.paid_at: Optional[datetime] = None
        
    def add_line(self, product_name: str, quantity: int, unit_price: Money) -> None:
        """Добавить строку заказа"""
        if self.is_paid:
            raise InvalidOrderOperation("Cannot modify paid order")
        
        self._lines.append(OrderLine(
            product_name=product_name,
            quantity=quantity,
            unit_price=unit_price
        ))
    
    def remove_line(self, index: int) -> None:
        """Удалить строку заказа"""
        if self.is_paid:
            raise InvalidOrderOperation("Cannot modify paid order")
        
        if 0 <= index < len(self._lines):
            self._lines.pop(index)
    
    @property
    def lines(self) -> List[OrderLine]:
        """Получить копию списка строк заказа"""
        return self._lines.copy()
    
    @property
    def total(self) -> Money:
        """Итоговая сумма заказа"""
        if not self._lines:
            return Money(0, "USD")
        
        # Суммируем все строки заказа
        total_amount = sum(line.total.amount for line in self._lines)
        return Money(total_amount, self._lines[0].unit_price.currency)
    
    @property
    def is_empty(self) -> bool:
        """Проверка, пустой ли заказ"""
        return len(self._lines) == 0
    
    @property
    def is_paid(self) -> bool:
        """Проверка, оплачен ли заказ"""
        return self.status == OrderStatus.PAID
    
    def pay(self) -> None:
        """Оплатить заказ (доменная операция)"""
        if self.is_empty:
            raise InvalidOrderOperation("Cannot pay empty order")
        
        if self.is_paid:
            raise InvalidOrderOperation("Order already paid")
        
        self.status = OrderStatus.PAID
        self.paid_at = datetime.now()
    
    def __repr__(self) -> str:
        return f"Order(id={self.order_id}, status={self.status.value}, total={self.total})"


class InvalidOrderOperation(Exception):
    """Исключение для недопустимых операций с заказом"""
    pass