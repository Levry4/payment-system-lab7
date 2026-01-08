# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Цель работы
Реализовать систему оплаты заказа с использованием слоистой архитектуры и принципов DDD-lite, с четким разделением ответственности между слоями.

## Структура проекта

payment-system-lab7/
├── domain/
│   ├── __init__.py
│   ├── entities.py
│   └── value_objects.py
├── application/
│   ├── __init__.py
│   └── use_cases.py
├── infrastructure/
│   ├── __init__.py
│   ├── repositories.py
│   └── gateways.py
├── tests/
│   ├── __init__.py
│   └── test_use_cases.py
├── main.py
├── requirements.txt
└── README.md

## Как запустить

Демонстрация работы:
python main.py

Запуск тестов:
python -m pytest tests/ -v

## Реализованные компоненты

Domain Layer
- Order - сущность заказа (агрегат)
- OrderLine - строка заказа (часть агрегата)
- Money - Value Object для денежных сумм
- OrderStatus - перечисление статусов заказа (CREATED, PAID, CANCELLED)

Application Layer
- PayOrderUseCase - use-case оплаты заказа
- OrderRepository - интерфейс репозитория заказов
- PaymentGateway - интерфейс платежного шлюза
- PayOrderResult - DTO для результата операции

Infrastructure Layer
- InMemoryOrderRepository - in-memory реализация репозитория
- FakePaymentGateway - фейковый платежный шлюз

## Инварианты доменной модели

1. Нельзя оплатить пустой заказ - проверка в методе Order.pay()
2. Нельзя оплатить заказ повторно - проверка статуса заказа
3. После оплаты нельзя менять строки заказа - блокировка в add_line()
4. Итоговая сумма равна сумме строк - автоматический расчет в Order.total

## Результат

✅ Все требования лабораторной работы выполнены
✅ Четкое разделение ответственности между слоями
✅ Все доменные инварианты реализованы
✅ Тесты покрывают все use-case и инварианты
✅ Архитектура соответствует принципам DDD-lite
