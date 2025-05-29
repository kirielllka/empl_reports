# Salary Reports Generator

Проект для генерации различных отчетов по зарплатам сотрудников на основе CSV файлов.

## Возможности

- Чтение CSV файлов с данными сотрудников
- Автоматическое определение структуры файла (не зависит от порядка столбцов)
- Генерация отчетов в консоли
- Поддержка разных типов отчетов

## Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/salary-reports.git
cd salary-reports
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

## Использование

### Базовое использование
```bash
python main.py файл1.csv файл2.csv --report payout
```

### Доступные типы отчетов:
- `payout` - Отчет по выплатам (зарплата = часы * ставка)
- `summary` - Сводный отчет по отделам (в разработке)
- `tax` - Отчет для налоговой (в разработке)

### Пример CSV файла
```
ID,Email,Name,Department,Hours,Rate
1,alice@example.com,Alice Johnson,Marketing,160,50
2,bob@example.com,Bob Smith,Design,150,40
```

## Добавление новых типов отчетов

1. Создайте новый класс отчета, унаследованный от `BaseReport`:

```python
class NewReport(BaseReport):
    @staticmethod
    def format_data(headers: List[str], file_data: List[Tuple[str, ...]]) -> Dict:
        """Форматирование данных для нового отчета"""
        # Ваша логика обработки данных
        return processed_data

    @staticmethod
    def output_report(data: Dict) -> None:
        """Вывод нового отчета"""
        # Ваша логика вывода отчета
        print("Новый отчет")
```

2. Добавьте обработку нового отчета в главную функцию:

```python
def main():
    # ... существующий код ...
    
    for file_path in args.files:
        headers, raw_data = BaseReport.read_csv(file_path)
        
        if args.report == 'payout':
            formatted_data = PayOutReport.format_data(headers, raw_data)
            PayOutReport.output_report(formatted_data)
        elif args.report == 'new_report':  # Добавьте новую ветку
            formatted_data = NewReport.format_data(headers, raw_data)
            NewReport.output_report(formatted_data)
```

3. Обновите аргументы командной строки:

```python
parser.add_argument(
    '--report',
    required=True,
    choices=['payout', 'summary', 'tax', 'new_report'],  # Добавьте новый тип
    help='Тип отчета: payout, summary, tax, new_report'
)
```

## Тестирование

Запуск тестов:
```bash
pytest -v
```

Тесты покрывают:
- Чтение CSV файлов
- Обработку данных
- Формирование отчетов
- Обработку ошибок

## Структура проекта

```
salary-reports/
├── reports/               # Модуль с отчетами
│   ├── __init__.py
│   ├── base_report.py     # Базовый класс отчетов
│   ├── payout_report.py   # Отчет по выплатам
│   └── new_report.py      # Пример нового отчета
├── tests/                 # Тесты
├── main.py                # Точка входа
└── README.md
```

## Лицензия

MIT License
