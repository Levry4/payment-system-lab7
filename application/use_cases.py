"""
Use Cases (Сценарии использования) и интерфейсы
"""

from typing import Protocol, Tuple
from dataclasses import dataclass
from domain.entities import Order, Money


class OrderRepository(Protocol):
    """Интерфейс репозитория заказов"""
    def get_by_id(self, order_id: str) -> Order:
        """Получить заказ по ID"""
        ...
    
    def save(self, order: Order) -> None:
        """Сохранить заказ"""
        ...


class PaymentGateway(Protocol):
    """Интерфейс платежного шлюза"""
    def charge(self, order_id: str, amount: Money) -> Tuple[bool, str]:
        """
        Выполнить платеж
        
        Returns:
            Tuple[bool, str]: (успех операции, идентификатор транзакции)
        """
        ...


@dataclass
class PayOrderResult:
    """Результат операции оплаты"""
    success: bool
    order_id: str
    transaction_id: str
    error_message: str = ""


class PayOrderUseCase:
    """Use Case для оплаты заказа"""
    
    def __init__(self, order_repository: OrderRepository, 
                 payment_gateway: PaymentGateway):
        self.order_repository = order_repository
        self.payment_gateway = payment_gateway
    
    def execute(self, order_id: str) -> PayOrderResult:
        """
        Выполнить оплату заказа
        
        Args:
            order_id: ID заказа для оплаты
            
        Returns:
            PayOrderResult: результат операции
        """
        try:
            # 1. Загружаем заказ
            order = self.order_repository.get_by_id(order_id)
            
            # 2. Выполняем доменную операцию оплаты
            order.pay()
            
            # 3. Вызываем платежный шлюз
            success, transaction_id = self.payment_gateway.charge(
                order_id=order_id,
                amount=order.total
            )
            
            if not success:
                return PayOrderResult(
                    success=False,
                    order_id=order_id,
                    transaction_id="",
                    error_message="Payment gateway declined the transaction"
                )
            
            # 4. Сохраняем обновленный заказ
            self.order_repository.save(order)
            
            return PayOrderResult(
                success=True,
                order_id=order_id,
                transaction_id=transaction_id
            )
            
        except Exception as e:
            return PayOrderResult(
                success=False,
                order_id=order_id,
                transaction_id="",
                error_message=str(e)
            )