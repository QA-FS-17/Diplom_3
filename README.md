# Тестирование веб-приложения Stellar Burgers

Проект автоматизированного тестирования веб-приложения для заказа бургеров с использованием паттерна Page Object Model.

## 📌 О проекте

Этот проект представляет собой комплекс автотестов для веб-приложения Stellar Burgers, включающий:
- Тестирование функционала восстановления пароля
- Тестирование личного кабинета пользователя
- Тестирование основного функционала приложения
- Тестирование ленты заказов

## 🛠 Технологический стек

- **Язык программирования**: Python 3.9+
- **Фреймворк для тестирования**: Pytest
- **Управление браузером**: Selenium WebDriver 4.15+
- **Драйвер браузера**: Undetected ChromeDriver
- **Отчетность**: Allure Framework
- **Дополнительно**: Page Object Model, WebDriver Waits, API клиент

## 📂 Структура проекта
```bash
Diplom_3/
├── allure-results/ # Результаты Allure
├── locators/
│   ├── __init__.py
│   ├── login_page_locators.py # # Локаторы элементов
│   ├── main_page_locators.py
│   ├── modal_locators.py
│   ├── order_feed_locators.py
│   ├── password_restore_locators.py
│   └── profile_page_locators.py
├── pages/
│   ├── __init__.py
│   ├── base_page.py # # Page Object модели
│   ├── login_page.py
│   ├── main_page.py
│   ├── order_feed_page.py
│   ├── password_restore_page.py
│   └── profile_page.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py # Фикстуры
│   ├── test_constructor.py # Тесты
│   ├── test_order_feed.py
│   ├── test_password_restore.py
│   └── test_user_profile.py
├── .gitignore
├── config.py # Конфигурация
├── helpers.py # Вспомогательные функции
├── data.py # Тестовые данные
├── README.md
└── requirements.txt # Зависимости
```
## 🚀 Запуск тестов

### Предварительные требования
1. Установите Python 3.9+
2. Установите зависимости:
   ```bash
   pip install -r requirements.txt
## Запуск всех тестов
```bash
pytest tests/ --alluredir=allure-results
```
## Запуск с определенным браузером
```bash
pytest tests/ --browser=chrome --alluredir=allure-results
```
## Генерация отчета Allure
```bash
allure serve allure-results
```

## 🔧 Настройка окружения
### Конфигурация тестового окружения находится в файле config.py:
- Базовые URL приложения
- Таймауты ожидания
- API endpoints
- Тестовые данные

## 📊 Тест-кейсы
### Раздел "Восстановление пароля"
- Переход на страницу восстановления пароля
- Ввод почты и клик по кнопке восстановления
- Проверка подсветки поля пароля

### Раздел "Личный кабинет"
- Переход в личный кабинет
- Навигация в историю заказов
- Выход из аккаунта

### Основной функционал
- Навигация по разделам конструктора
- Взаимодействие с модальными окнами
- Оформление заказа авторизованным пользователем

### Лента заказов
- Просмотр деталей заказа
- Проверка счетчиков выполненных заказов
- Отслеживание статуса заказов