<h1 align="center">💳 Лабораторная работа 7</h1>
<h3 align="center">Архитектура, слои и DDD-lite</h3>

<p align="center">
  Система оплаты заказа с использованием слоистой архитектуры и DDD-lite
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.8+-blue.svg" alt="Python">
  <img src="https://img.shields.io/badge/Architecture-Layered-green.svg" alt="Architecture">
  <img src="https://img.shields.io/badge/DDD-lite-orange.svg" alt="DDD">
  <img src="https://img.shields.io/badge/Tests-Passing-brightgreen.svg" alt="Tests">
</p>

---

## 🏗️ Архитектура проекта

```text
payment-system-lab7/
├── 📁 domain/                    # Доменный слой
│   ├── 📄 __init__.py
│   ├── 📄 entities.py           # Order, OrderLine, OrderStatus
│   └── 📄 value_objects.py      # Money (Value Object)
├── 📁 application/              # Слой приложения
│   ├── 📄 __init__.py
│   └── 📄 use_cases.py          # PayOrderUseCase + интерфейсы
├── 📁 infrastructure/           # Инфраструктурный слой
│   ├── 📄 __init__.py
│   ├── 📄 repositories.py       # InMemoryOrderRepository
│   └── 📄 gateways.py          # FakePaymentGateway
├── 📁 tests/                    # Тесты
│   ├── 📄 __init__.py
│   └── 📄 test_use_cases.py     # Тесты всех use-case
├── ⚡ main.py                   # Точка входа
├── 📋 requirements.txt          # Зависимости
└── 📖 README.md                 # Документация
