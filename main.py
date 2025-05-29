import abc
import argparse
from typing import List, Dict, Tuple


class BaseReport(abc.ABC):
    @staticmethod
    def read_csv(path: str):
        """Чтение CSV файла с обработкой заголовков"""
        with open(path, 'r') as file:
            lines = [line.strip() for line in file if line.strip()]
            if not lines:
                return [], []

            headers = lines[0].split(',')
            data = [list(line.split(',')) for line in lines[1:]]
            return headers, data


class PayOutReport(BaseReport):
    @staticmethod
    def format_data(headers:list, file_data:list) -> dict:
        """Форматирование данных с учетом заголовков"""
        try:
            id_index = headers.index('id')
            email_index = headers.index('email')
            name_index = headers.index('name')
            dept_index = headers.index('department')
            hours_index = headers.index('hours_worked')
            try:
                rate_index = headers.index('hourly_rate')
            except ValueError:
                if headers.count('rate'):
                    rate_index = headers.index('rate')
                else:
                    rate_index = headers.index('salary')

        except ValueError as e:
            raise ValueError(f"Отсутствует обязательный столбец: {str(e)}")

        personal_dict = {}
        for line in file_data:
            if len(line) >= max(id_index, email_index, name_index, dept_index, hours_index, rate_index) + 1:
                personal_dict[line[id_index]] = {
                    'email': line[email_index],
                    'Name': line[name_index],
                    'Department': line[dept_index],
                    'Hours': line[hours_index],
                    'Rate': line[rate_index]
                }
        return personal_dict

    @staticmethod
    def output_report(data:dict) -> None:
        """Вывод отчета в консоль"""
        print("\n{:<5} {:<30} {:<20} {:<15} {:<10} {:<10}".format(
            "ID", "Name", "Email", "Department", "Hours", "Salary"))
        print("-" * 90)

        for emp_id, details in data.items():
            try:
                salary = int(details['Hours']) * int(details['Rate'])
                print("{:<5} {:<30} {:<20} {:<15} {:<10} ${:<10}".format(
                    emp_id,
                    details['Name'],
                    details['email'],
                    details['Department'],
                    details['Hours'],
                    salary
                ))
            except (ValueError, KeyError) as e:
                print(f"Ошибка обработки данных сотрудника {emp_id}: {str(e)}")


def main():
    """Основная функция для обработки аргументов командной строки"""
    parser = argparse.ArgumentParser(description='Генератор отчетов по зарплатам')
    parser.add_argument(
        'files',
        nargs='+',
        help='CSV файлы с данными сотрудников'
    )
    parser.add_argument(
        '--report',
        required=True,
        choices=['payout'],
        help='Тип отчета: payout'
    )

    args = parser.parse_args()

    for file_path in args.files:
        try:
            headers, raw_data = BaseReport.read_csv(file_path)
            if not headers:
                print(f"Файл {file_path} пуст или не содержит данных")
                continue

            formatted_data = PayOutReport.format_data(headers, raw_data)

            print(f"\nОтчет для файла: {file_path}")
            if args.report == 'payout':
                PayOutReport.output_report(formatted_data)
            # Обработка других типов отчетов...

        except FileNotFoundError:
            print(f"Ошибка: файл {file_path} не найден")
        except ValueError as e:
            print(f"Ошибка в структуре файла {file_path}: {str(e)}")
        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {str(e)}")


if __name__ == '__main__':
    main()