"""
Инфраструктурные реализации платежных шлюзов
"""

import uuid
from typing import Tuple
from domain.value_objects import Money
from application.use_cases import PaymentGateway


class FakePaymentGateway(PaymentGateway):
    """Фейковый платежный шлюз для тестирования"""
    
    def __init__(self, should_succeed: bool = True):
        self.should_succeed = should_succeed
        self.charge_calls = []
    
    def charge(self, order_id: str, amount: Money) -> Tuple[bool, str]:
        """Имитация платежа"""
        self.charge_calls.append({
            'order_id': order_id,
            'amount': amount
        })
        
        if self.should_succeed:
            transaction_id = f"txn_{uuid.uuid4().hex[:8]}"
            return True, transaction_id
        else:
            return False, ""