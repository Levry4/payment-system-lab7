"""
Модульные тесты для Use Cases и доменной модели
"""

import unittest
from domain.entities import Order, OrderLine, InvalidOrderOperation
from domain.value_objects import Money
from application.use_cases import PayOrderUseCase, PayOrderResult
from infrastructure.repositories import InMemoryOrderRepository
from infrastructure.gateways import FakePaymentGateway


class TestPayOrderUseCase(unittest.TestCase):
    """Тесты для Use Case оплаты заказа"""
    
    def setUp(self):
        """Настройка перед каждым тестом"""
        self.repository = InMemoryOrderRepository()
        self.payment_gateway = FakePaymentGateway(should_succeed=True)
        self.use_case = PayOrderUseCase(
            order_repository=self.repository,
            payment_gateway=self.payment_gateway
        )
    
    def create_sample_order(self) -> Order:
        """Создать тестовый заказ"""
        order = Order(order_id="order_1", customer_id="customer_1")
        order.add_line("Product A", 2, Money(10.0))
        order.add_line("Product B", 1, Money(15.5))
        self.repository.save(order)
        return order
    
    def test_successful_payment(self):
        """Тест успешной оплаты корректного заказа"""
        # Arrange
        order = self.create_sample_order()
        
        # Act
        result = self.use_case.execute("order_1")
        
        # Assert
        self.assertTrue(result.success)
        self.assertEqual(result.order_id, "order_1")
        self.assertIn("txn_", result.transaction_id)
        
        # Проверяем, что заказ действительно оплачен
        updated_order = self.repository.get_by_id("order_1")
        self.assertTrue(updated_order.is_paid)
        self.assertIsNotNone(updated_order.paid_at)
        
        # Проверяем, что платежный шлюз был вызван
        self.assertEqual(len(self.payment_gateway.charge_calls), 1)
        self.assertEqual(
            self.payment_gateway.charge_calls[0]['order_id'],
            "order_1"
        )
    
    def test_payment_empty_order_fails(self):
        """Тест ошибки при оплате пустого заказа"""
        # Arrange
        order = Order(order_id="empty_order", customer_id="customer_1")
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("empty_order")
        
        # Assert
        self.assertFalse(result.success)
        self.assertIn("Cannot pay empty order", result.error_message)
        
        # Проверяем, что платежный шлюз не был вызван
        self.assertEqual(len(self.payment_gateway.charge_calls), 0)
    
    def test_double_payment_fails(self):
        """Тест ошибки при повторной оплате"""
        # Arrange
        order = self.create_sample_order()
        
        # Первая оплата должна быть успешной
        first_result = self.use_case.execute("order_1")
        self.assertTrue(first_result.success)
        
        # Act - пытаемся оплатить снова
        second_result = self.use_case.execute("order_1")
        
        # Assert
        self.assertFalse(second_result.success)
        self.assertIn("Order already paid", second_result.error_message)
        
        # Платежный шлюз должен был быть вызван только один раз
        self.assertEqual(len(self.payment_gateway.charge_calls), 1)
    
    def test_cannot_modify_paid_order(self):
        """Тест невозможности изменения заказа после оплаты"""
        # Arrange
        order = self.create_sample_order()
        
        # Оплачиваем заказ
        result = self.use_case.execute("order_1")
        self.assertTrue(result.success)
        
        # Act & Assert - попытка добавить строку должна вызвать ошибку
        paid_order = self.repository.get_by_id("order_1")
        
        with self.assertRaises(InvalidOrderOperation) as context:
            paid_order.add_line("Product C", 3, Money(5.0))
        
        self.assertIn("Cannot modify paid order", str(context.exception))
    
    def test_total_calculation_correct(self):
        """Тест корректного расчета итоговой суммы"""
        # Arrange
        order = Order(order_id="calc_test", customer_id="customer_1")
        order.add_line("Product A", 2, Money(10.0))  # 20
        order.add_line("Product B", 1, Money(15.5))  # 15.5
        order.add_line("Product C", 3, Money(2.0))   # 6
        self.repository.save(order)
        
        # Act
        result = self.use_case.execute("calc_test")
        
        # Assert
        self.assertTrue(result.success)
        
        # Проверяем сумму в вызове платежного шлюза
        self.assertEqual(
            self.payment_gateway.charge_calls[0]['amount'],
            Money(41.5)  # 20 + 15.5 + 6 = 41.5
        )
    
    def test_payment_gateway_failure(self):
        """Тест обработки отказа платежного шлюза"""
        # Arrange
        order = self.create_sample_order()
        failing_gateway = FakePaymentGateway(should_succeed=False)
        use_case = PayOrderUseCase(
            order_repository=self.repository,
            payment_gateway=failing_gateway
        )
        
        # Act
        result = use_case.execute("order_1")
        
        # Assert
        self.assertFalse(result.success)
        self.assertIn("Payment gateway declined", result.error_message)
        
        # Заказ не должен быть помечен как оплаченный
        updated_order = self.repository.get_by_id("order_1")
        self.assertFalse(updated_order.is_paid)


class TestDomainModel(unittest.TestCase):
    """Тесты доменной модели"""
    
    def test_money_value_object_immutability(self):
        """Тест неизменяемости value object Money"""
        money1 = Money(100.0, "USD")
        money2 = Money(100.0, "USD")
        money3 = Money(200.0, "USD")
        
        self.assertEqual(money1, money2)
        self.assertNotEqual(money1, money3)
        
        # Проверяем операции
        result = money1 + money2
        self.assertEqual(result, Money(200.0, "USD"))
        
        # Проверяем, что оригинальные объекты не изменились
        self.assertEqual(money1, Money(100.0, "USD"))
    
    def test_order_line_total_calculation(self):
        """Тест расчета суммы для строки заказа"""
        line = OrderLine("Test Product", 3, Money(10.0))
        self.assertEqual(line.total, Money(30.0))
    
    def test_order_status_transitions(self):
        """Тест переходов статуса заказа"""
        order = Order("test_order", "customer_1")
        order.add_line("Product", 1, Money(10.0))
        
        self.assertEqual(order.status.value, "created")
        self.assertFalse(order.is_paid)
        
        order.pay()
        
        self.assertEqual(order.status.value, "paid")
        self.assertTrue(order.is_paid)
        self.assertIsNotNone(order.paid_at)


if __name__ == "__main__":
    unittest.main()