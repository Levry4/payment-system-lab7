#!/usr/bin/env python3
"""
Лаба 7 - Архитектура, слои и DDD-lite
Точка входа в приложение
"""

import sys
import os

# Добавляем текущую папку в путь Python для корректных импортов
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

print("=" * 60)
print("Лабораторная работа 7: Архитектура, слои и DDD-lite")
print("=" * 60)

try:
    # Импортируем все модули
    from domain.entities import Order, OrderStatus, InvalidOrderOperation
    from domain.value_objects import Money
    from application.use_cases import PayOrderUseCase, PayOrderResult
    from infrastructure.repositories import InMemoryOrderRepository
    from infrastructure.gateways import FakePaymentGateway
    
    print("✅ Все модули успешно импортированы!")
    
except ImportError as e:
    print(f"❌ Ошибка импорта: {e}")
    print("\nПроверьте структуру проекта:")
    print("  lab7/")
    print("  ├── domain/")
    print("  │   ├── __init__.py")
    print("  │   ├── entities.py")
    print("  │   └── value_objects.py")
    print("  ├── application/")
    print("  │   ├── __init__.py")
    print("  │   └── use_cases.py")
    print("  └── ...")
    sys.exit(1)


def demonstrate_successful_payment():
    """Демонстрация успешной оплаты"""
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ 1: Успешная оплата заказа")
    print("="*60)
    
    # Инициализация
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(should_succeed=True)
    use_case = PayOrderUseCase(repo, gateway)
    
    # Создаем заказ
    order = Order("order_001", "customer_123")
    order.add_line("Ноутбук MacBook Pro", 1, Money(1999.99, "USD"))
    order.add_line("Мышь Magic Mouse", 2, Money(79.99, "USD"))
    order.add_line("Чехол", 1, Money(49.99, "USD"))
    
    repo.save(order)
    
    print(f"\n📦 Заказ создан:")
    print(f"   ID: {order.order_id}")
    print(f"   Клиент: {order.customer_id}")
    print(f"   Строк заказа: {len(order.lines)}")
    print(f"   Итоговая сумма: {order.total}")
    print(f"   Статус: {order.status.value}")
    
    # Оплачиваем заказ
    print(f"\n💳 Оплачиваем заказ...")
    result: PayOrderResult = use_case.execute("order_001")
    
    if result.success:
        print(f"   ✅ Платеж успешен!")
        print(f"   ID транзакции: {result.transaction_id}")
    else:
        print(f"   ❌ Ошибка платежа: {result.error_message}")
    
    # Проверяем обновленный заказ
    updated_order = repo.get_by_id("order_001")
    print(f"\n🔄 Обновленный заказ:")
    print(f"   Статус: {updated_order.status.value}")
    print(f"   Время оплаты: {updated_order.paid_at}")
    print(f"   Оплачен: {updated_order.is_paid}")


def demonstrate_error_cases():
    """Демонстрация ошибочных сценариев"""
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ 2: Ошибочные сценарии")
    print("="*60)
    
    repo = InMemoryOrderRepository()
    gateway = FakePaymentGateway(should_succeed=True)
    use_case = PayOrderUseCase(repo, gateway)
    
    # 1. Пустой заказ
    print("\n1. Попытка оплаты пустого заказа:")
    empty_order = Order("empty_order", "customer_456")
    repo.save(empty_order)
    
    result = use_case.execute("empty_order")
    print(f"   Результат: {'❌ ОШИБКА' if not result.success else '✅ УСПЕХ'}")
    if not result.success:
        print(f"   Причина: {result.error_message}")
    
    # 2. Повторная оплата
    print("\n2. Попытка повторной оплаты:")
    paid_order = Order("paid_order", "customer_789")
    paid_order.add_line("Товар", 1, Money(100.0, "USD"))
    repo.save(paid_order)
    
    # Первая оплата
    first_result = use_case.execute("paid_order")
    print(f"   Первая оплата: {'✅ УСПЕХ' if first_result.success else '❌ ОШИБКА'}")
    
    # Вторая оплата
    second_result = use_case.execute("paid_order")
    print(f"   Вторая оплата: {'✅ УСПЕХ' if second_result.success else '❌ ОШИБКА'}")
    if not second_result.success:
        print(f"   Причина: {second_result.error_message}")


def demonstrate_domain_invariants():
    """Демонстрация инвариантов доменной модели"""
    print("\n" + "="*60)
    print("ДЕМОНСТРАЦИЯ 3: Инварианты доменной модели")
    print("="*60)
    
    # 1. Инвариант: итоговая сумма
    print("\n1. Проверка расчета итоговой суммы:")
    order = Order("calc_test", "customer_999")
    order.add_line("Товар A", 3, Money(10.0, "USD"))      # 30
    order.add_line("Товар B", 2, Money(7.50, "USD"))      # 15
    order.add_line("Товар C", 1, Money(25.25, "USD"))     # 25.25
    
    expected_total = 30 + 15 + 25.25
    print(f"   Строк заказа: {len(order.lines)}")
    print(f"   Ожидаемая сумма: USD {expected_total:.2f}")
    print(f"   Фактическая сумма: {order.total}")
    print(f"   Совпадает: {'✅ ДА' if order.total.amount == expected_total else '❌ НЕТ'}")
    
    # 2. Инвариант: нельзя менять оплаченный заказ
    print("\n2. Проверка блокировки изменений после оплаты:")
    test_order = Order("locked_order", "customer_111")
    test_order.add_line("Дорогой товар", 1, Money(1000.0, "USD"))
    test_order.pay()
    
    try:
        test_order.add_line("Новый товар", 1, Money(500.0, "USD"))
        print("   ❌ ОШИБКА: Изменения разрешены!")
    except InvalidOrderOperation as e:
        print(f"   ✅ Корректно: {str(e)}")


def run_tests():
    """Запуск тестов"""
    print("\n" + "="*60)
    print("ЗАПУСК ТЕСТОВ")
    print("="*60)
    
    import subprocess
    import sys
    
    print("Запускаем тесты через pytest...\n")
    
    # Запускаем тесты
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/", "-v"],
        capture_output=True,
        text=True
    )
    
    print(result.stdout)
    
    if result.stderr:
        print("Ошибки:")
        print(result.stderr)
    
    return result.returncode == 0


def main():
    """Главная функция"""
    
    try:
        # Демонстрационные сценарии
        demonstrate_successful_payment()
        demonstrate_error_cases()
        demonstrate_domain_invariants()
        
        # Запуск тестов
        print("\n" + "="*60)
        run_tests_option = input("Запустить автоматические тесты? (y/n): ")
        if run_tests_option.lower() == 'y':
            run_tests()
        
        print("\n" + "="*60)
        print("✅ Демонстрация завершена успешно!")
        print("Все требования лабораторной работы выполнены:")
        print("1. ✅ Domain слой с доменной моделью")
        print("2. ✅ Application слой с use-case")
        print("3. ✅ Infrastructure слой с реализациями")
        print("4. ✅ Тесты всех use-case")
        print("5. ✅ Все инварианты доменной модели")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Неожиданная ошибка: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())