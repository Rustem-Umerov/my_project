# my_project

## Описание:

Данный проект - это виджет, который показывает несколько последних успешных банковских операций клиента.

## Установка:

1. Клонируйте репозиторий:
```
git clone https://github.com/Rustem-Umerov/my_project.git
```
1. Перейдите в корневую папку:
```
cd my_project
```
1. Установите зависимости с помощью Poetry:
```
poetry install
```

## Использование:

Пример будет добавлен в будущем.

## Модуль generators.py

### Данный модуль позволяет:
- Отфильтровывать транзакций по определенной валюте. 
- Получать описания каждой операции.
- Генерация номера банковских карт для клиентов.

Этот модуль предоставляет функции для работы с номерами банковских карт. 
В его состав входят следующие функции:

- #### filter_by_currency: 
Функция возвращает итератор, который поочередно выдает транзакции, 
где валюта операции соответствует заданной (например, USD).

- #### transaction_descriptions:
Генератор, который принимает список словарей с транзакциями 
и возвращает описание каждой операции по очереди.

- #### card_number_generator:
Генератор, который выдает номера банковских карт в формате XXXX XXXX XXXX XXXX , 
где X — цифра номера карты. Генератор может сгенерировать номера карт в заданном диапазоне 
от 0000 0000 0000 0001 до 9999 9999 9999 9999.
Генератор должен принимать начальное и конечное значения для генерации диапазона номеров.


## Примеры использования

#### Функции filter_by_currency и transaction_descriptions:

```
from src.generators import filter_by_currency, transaction_descriptions 


# Список странзакциями
transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
    {
        "id": 873106923,
        "state": "EXECUTED",
        "date": "2019-03-23T01:09:46.296404",
        "operationAmount": {"amount": "43318.34", "currency": {"name": "руб.", "code": "RUB"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 44812258784861134719",
        "to": "Счет 74489636417521191160",
    }
]

# Фильтрация транзакций по валюте "USD"
usd_transactions = list(filter_by_currency(transactions, "USD"))
print("USD транзакции:")
for transaction in usd_transactions:
    print(transaction)

# Получение описаний транзакций
descriptions = list(transaction_descriptions(transactions))
print("Описания транзакций:")
for description in descriptions:
    print(description)
```

#### Функция card_number_generator:

```
from src.generators import card_number_generator


# Генерация номеров карт для диапазона от 1 до 5
for number in card_number_generator(1, 5):
    print(number)


>>> Вывод:
0000 0000 0000 0001
0000 0000 0000 0002
0000 0000 0000 0003
0000 0000 0000 0004
0000 0000 0000 0005
```

## Модуль decorators.py

### Данный модуль содержит:
- #### Декоратор log
Декоратор лог логирует:
* начало выполнения функции;
* переданные позиционные и именованные аргументы;
* успешное завершение с результатом.

В случае, если возникнет исключение:
* исключение, если оно возникает, с типом и трассировкой.

## Примеры использования

#### Декоратор log:

```
from src.decorators import log


# Создаем дополнительную функцию для проверки декоратора.
@log(filename=None)
def add(a: float, b: float) -> float:
    """Дополнительная функция, необходимая для тестирования логов из декоратора."""

    return a + b

# Вызываем функцию и передаем ей аргументы.
add(5, 5)

>>> Вывод:
2025-05-21 14:21:20 [INFO ] decorators.wrapper:33 - Starting function add with arguments: args=(5, 5), kwargs={}
2025-05-21 14:21:20 [INFO ] decorators.wrapper:37 - Function add completed successfully. Result: 10
```
```
from src.decorators import log


# Ниже будет проверен случай, когда есть исключение.
# Создаем дополнительную функцию для проверки декоратора.
@log(filename=None)
def divide(a: float, b: float) -> float:
    """Дополнительная функция, необходимая для тестирования логов из декоратора."""

    return a / b

# Вызываем функцию и передаем ей аргументы.
divide(5, 0)

>>> Вывод:
2025-05-21 14:55:31 [INFO ] decorators.wrapper:33 - Starting function divide with arguments: args=(5, 0), kwargs={}
2025-05-21 14:55:31 [ERROR] decorators.wrapper:41 - Error in function divide. Error type: ZeroDivisionError. Arguments: args=(5, 0), kwargs={}
Traceback (most recent call last):
  File "C:\Users\Rustem\PycharmProjects\PythonProject\file_8.py", line 36, in wrapper
    result = func(*args, **kwargs)
  File "C:\Users\Rustem\PycharmProjects\PythonProject\file_6.py", line 10, in divide
    return a / b
           ~~^~~
ZeroDivisionError: division by zero
Traceback (most recent call last):
  File "C:\Users\Rustem\PycharmProjects\PythonProject\file_6.py", line 12, in <module>
    divide(5, 0)
    ~~~~~~^^^^^^
  File "C:\Users\Rustem\PycharmProjects\PythonProject\file_8.py", line 36, in wrapper
    result = func(*args, **kwargs)
  File "C:\Users\Rustem\PycharmProjects\PythonProject\file_6.py", line 10, in divide
    return a / b
           ~~^~~
ZeroDivisionError: division by zero
```

## Тестирование:

Чтобы установить pytest, используйте команду:
```
poetry add --group dev pytest
```

В pytest для анализа покрытия кода надо поставить библиотеку pytest-cov:
```
poetry add --group dev pytest-cov
```

Чтобы запустить тесты с оценкой покрытия, можно воспользоваться следующими командами:

При активированном виртуальном окружении:
```
pytest --cov
```
Через poetry:
```
poetry run pytest --cov
```

## Документация:

Для получения дополнительной информации обратитесь к [документации](README.md).