import pytest

from main import BaseReport, PayOutReport

# Фикстуры для тестовых данных
@pytest.fixture
def sample_csv_file(tmp_path):
    """Создает тестовый CSV файл с правильной структурой"""
    data = [
        "id,email,name,department,hours_worked,rate",
        "1,alice@example.com,Alice Johnson,Marketing,160,50",
        "2,bob@example.com,Bob Smith,Design,150,40"
    ]
    file_path = tmp_path / "employees.csv"
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def shuffled_csv_file(tmp_path):
    """Создает CSV файл с перемешанными столбцами"""
    data = [
        "name,department,id,email,rate,hours_worked",
        "Alice Johnson,Marketing,1,alice@example.com,50,160",
        "Bob Smith,Design,2,bob@example.com,40,150"
    ]
    file_path = tmp_path / "shuffled.csv"
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def invalid_csv_file(tmp_path):
    """Создает CSV файл с неполными данными"""
    data = [
        "id,email,name,department,hours_worked,rate",
        "1,alice@example.com,Alice Johnson,Marketing,160",
        "2,bob@example.com,Bob Smith,Design"
    ]
    file_path = tmp_path / "invalid.csv"
    file_path.write_text("\n".join(data))
    return str(file_path)

@pytest.fixture
def empty_csv_file(tmp_path):
    """Создает пустой CSV файл"""
    file_path = tmp_path / "empty.csv"
    file_path.write_text("")
    return str(file_path)

class TestPayOutReport:

    def test_format_data_valid(self, sample_csv_file):
        """Тест форматирования данных с правильной структурой"""
        headers, data = BaseReport.read_csv(sample_csv_file)
        result = PayOutReport.format_data(headers, data)

        assert len(result) == 2
        assert result["1"]["Name"] == "Alice Johnson"
        assert result["2"]["Department"] == "Design"
        assert result["1"]["Hours"] == "160"

    def test_format_data_shuffled(self, shuffled_csv_file):
        """Тест форматирования данных с перемешанными столбцами"""
        headers, data = BaseReport.read_csv(shuffled_csv_file)
        result = PayOutReport.format_data(headers, data)

        assert len(result) == 2
        assert result["1"]["Name"] == "Alice Johnson"
        assert result["2"]["Rate"] == "40"

    def test_format_data_missing_columns(self, tmp_path):
        """Тест обработки файла с отсутствующими столбцами"""
        data = [
            "ID,Name,Department",
            "1,Alice Johnson,Marketing"
        ]
        file_path = tmp_path / "missing_columns.csv"
        file_path.write_text("\n".join(data))

        headers, data = BaseReport.read_csv(str(file_path))
        with pytest.raises(ValueError, match="Отсутствует обязательный столбец"):
            PayOutReport.format_data(headers, data)

    def test_format_data_invalid(self, invalid_csv_file):
        """Тест обработки файла с неполными данными"""
        headers, data = BaseReport.read_csv(invalid_csv_file)
        result = PayOutReport.format_data(headers, data)

        # Проверяем что только корректные строки обработаны
        assert len(result) == 0
