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


### Примеры использования

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

### Примеры использования

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

## Модуль utils.py

### Данный модуль содержит:
- #### Функцию financial_operations

Функция принимает на вход путь до JSON-файла и возвращает список словарей с данными о финансовых транзакциях.
Если файл пустой, содержит не список или не найден, функция возвращает пустой список.

### Пример использования

```
base_dir = Path(__file__).resolve().parent  # Определяем базовый путь относительно текущего файла

# Ниже формируем путь к json-файлу, который находится в папке 'data' внутри базовой директории
json_path = base_dir.parent / "data" / "operations.json"

# Ниже вызываем функцию, передав в неё путь к json-файлу
financial_operations_result = financial_operations(json_path)
```

## Модуль external_api.py

### Данный модуль содержит:
- #### Функции transaction и convert_to_rub

Функция transaction: Принимает словарь с данными транзакции, из которого извлекается сумма. 
Если валюта не RUB, используется функция convert_to_rub для конвертации суммы. 
При отсутствии или некорректности данных функция регистрирует ошибку и возвращает 0.0.

Функция convert_to_rub: Обращается к внешнему API для получения текущего обменного курса 
и преобразует переданную сумму в рубли. При ошибках ответа или проблемах с конвертацией 
логирует ошибку и возвращает 0.0.

### Пример использования
```
from utils import transaction, convert_to_rub

# Пример транзакции в рублях (без конвертации)
transaction_rub = {
    "operationAmount": {
        "amount": 1500.0,
        "currency": {
            "name": "руб",
            "code": "RUB"
        }
    }
}

# Пример транзакции в иностранной валюте (например, USD)
transaction_usd = {
    "operationAmount": {
        "amount": 100.0,
        "currency": {
            "name": "USD",
            "code": "USD"
        }
    }
}

# Обработка транзакций
result_rub = transaction(transaction_rub)
result_usd = transaction(transaction_usd)  # здесь вызывается convert_to_rub для конвертации

print("Сумма транзакции (RUB):", result_rub)
print("Сумма транзакции (USD, конвертированная в рубли):", result_usd)
```
```
from utils import convert_to_rub

# Прямой вызов convert_to_rub для конвертации 50 единиц валюты (например, USD) в рубли.
# Здесь "USD" - код валюты, а 50 - сумма операции.
amount_in_rub = convert_to_rub("USD", 50.0)
print("50 USD в рублях:", amount_in_rub)

```


## Модуль financial_transactions.py

### Данный модуль содержит:
- #### Функции fin_trans_from_csv_file и fin_trans_from_csv_file

Функция fin_trans_from_csv_file предназначена для чтения CSV-файла, содержащего финансовые транзакции. 
Принимает путь к файлу CSV в качестве аргумента. Возвращает список словарей с транзакциями

Обработка ошибок:
Если файл не найден, генерируется и логируется исключение FileNotFoundError.
ППри возникновении ошибки парсинга CSV-файла (pandas.errors.ParserError) логируется сообщение об ошибке, и исключение пробрасывается далее.
При других непредвиденных ошибках происходит логирование и проброс общего исключения Exception.

Функция fin_trans_from_excel_file считывает данные из Excel-файла, содержащего финансовые транзакции.
Принимает путь к файлу Excel-файлу в качестве аргумента. Возвращает список словарей с транзакциями.

Обработка ошибок:
Если файл не найден, генерируется и логируется исключение FileNotFoundError.
При возникновении ошибки парсинга Excel-файла (pandas.errors.ParserError) логируется сообщение об ошибке и исключение пробрасывается далее.
При других непредвиденных ошибках происходит логирование и проброс общего исключения Exception.

### Пример использования

```
from pathlib import Path
from src.financial_transactions import fin_trans_from_csv_file

# Укажите путь к вашему CSV-файлу
csv_file_path = Path("data/transactions.csv")

try:
    transactions = fin_trans_from_csv_file(csv_file_path)
    # transactions – это список словарей, где каждый словарь представляет отдельную транзакцию.
    print("Транзакции успешно считаны:", transactions)
except FileNotFoundError:
    print(f"Файл {csv_file_path} не найден.")
except Exception as e:
    print("Ошибка при чтении CSV-файла:", str(e))
```
```
from pathlib import Path
from src.financial_transactions import fin_trans_from_excel_file

# Укажите путь к вашему Excel-файлу
excel_file_path = Path("data/transactions.xlsx")

try:
    transactions = fin_trans_from_excel_file(excel_file_path)
    # transactions – это список транзакций, преобразованных из Excel в список словарей.
    print("Транзакции успешно считаны:", transactions)
except FileNotFoundError:
    print(f"Файл {excel_file_path} не найден.")
except Exception as e:
    print("Ошибка при чтении Excel-файла:", str(e))
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