# Лабораторная работа 7: Архитектура, слои и DDD-lite

## Цель работы
Реализовать систему оплаты заказа с использованием слоистой архитектуры и принципов DDD-lite, с четким разделением ответственности между слоями.

## Структура проекта
payment-system-lab7/
├── domain/ # Доменный слой
│ ├── init.py
│ ├── entities.py # Order, OrderLine, OrderStatus
│ └── value_objects.py # Money (Value Object)
├── application/ # Слой приложения
│ ├── init.py
│ └── use_cases.py # PayOrderUseCase + интерфейсы
├── infrastructure/ # Инфраструктурный слой
│ ├── init.py
│ ├── repositories.py # InMemoryOrderRepository
│ └── gateways.py # FakePaymentGateway
├── tests/ # Тесты
│ ├── init.py
│ └── test_use_cases.py # Тесты use-case
├── main.py # Точка входа
├── requirements.txt # Зависимости
└── README.md # Документация

text

## Как запустить

### Демонстрация работы:
```bash
python main.py
Запуск тестов:

bash
python -m pytest tests/ -v
Реализованные компоненты

Domain Layer

Order - сущность заказа (агрегат)
OrderLine - строка заказа (часть агрегата)
Money - Value Object для денежных сумм
OrderStatus - перечисление статусов заказа (CREATED, PAID, CANCELLED)
Application Layer

PayOrderUseCase - use-case оплаты заказа
OrderRepository - интерфейс репозитория заказов
PaymentGateway - интерфейс платежного шлюза
PayOrderResult - DTO для результата операции
Infrastructure Layer

InMemoryOrderRepository - in-memory реализация репозитория
FakePaymentGateway - фейковый платежный шлюз
Инварианты доменной модели

Нельзя оплатить пустой заказ - проверка в методе Order.pay()
Нельзя оплатить заказ повторно - проверка статуса заказа
После оплаты нельзя менять строки заказа - блокировка в add_line()
Итоговая сумма равна сумме строк - автоматический расчет в Order.total
Результат

✅ Все требования лабораторной работы выполнены
✅ Четкое разделение ответственности между слоями
✅ Все доменные инварианты реализованы
✅ Тесты покрывают все use-case и инварианты
✅ Архитектура соответствует принципам DDD-lite
