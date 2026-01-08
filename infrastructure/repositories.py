"""
Инфраструктурные реализации репозиториев
"""

from typing import Dict
from domain.entities import Order
from application.use_cases import OrderRepository


class InMemoryOrderRepository(OrderRepository):
    """In-memory реализация репозитория заказов"""
    
    def __init__(self):
        self._storage: Dict[str, Order] = {}
    
    def get_by_id(self, order_id: str) -> Order:
        order = self._storage.get(order_id)
        if order is None:
            raise ValueError(f"Order with id {order_id} not found")
        return order
    
    def save(self, order: Order) -> None:
        self._storage[order.order_id] = order
    
    def clear(self) -> None:
        """Очистить хранилище (для тестов)"""
        self._storage.clear()