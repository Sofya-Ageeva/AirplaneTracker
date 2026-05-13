import os
import json
import tempfile
import pytest
from src.aeroplane import Aeroplane
from src.storage import JSONSaver


class TestJSONSaver:
    """Тесты для хранилища"""

    def setup_method(self):
        """Создаем временный файл для тестов"""
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.filename = self.temp_file.name

        self.storage = JSONSaver(self.filename)

        # Создаем тестовые самолеты
        self.plane1 = Aeroplane("TEST1", "Russia", 800, 10000, "ABC123")
        self.plane2 = Aeroplane("TEST2", "USA", 750, 9000, "DEF456")

    def teardown_method(self):
        """Удаляем временный файл"""
        if os.path.exists(self.filename):
            os.remove(self.filename)

    def test_add_aeroplane(self):
        """Тест добавления самолета"""
        result = self.storage.add_aeroplane(self.plane1)
        assert result == True

        planes = self.storage.get_all()
        assert len(planes) == 1
        assert planes[0].callsign == "TEST1"

    def test_add_duplicate(self):
        """Тест добавления дубликата"""
        self.storage.add_aeroplane(self.plane1)
        result = self.storage.add_aeroplane(self.plane1)

        assert result == False
        planes = self.storage.get_all()
        assert len(planes) == 1

    def test_get_all(self):
        """Тест получения всех самолетов"""
        self.storage.add_aeroplane(self.plane1)
        self.storage.add_aeroplane(self.plane2)

        planes = self.storage.get_all()
        assert len(planes) == 2

    def test_delete_aeroplane(self):
        """Тест удаления самолета"""
        self.storage.add_aeroplane(self.plane1)
        self.storage.add_aeroplane(self.plane2)

        result = self.storage.delete_aeroplane(self.plane1)
        assert result == True

        planes = self.storage.get_all()
        assert len(planes) == 1
        assert planes[0].callsign == "TEST2"

    def test_clear_all(self):
        """Тест очистки всех данных"""
        self.storage.add_aeroplane(self.plane1)
        self.storage.add_aeroplane(self.plane2)

        result = self.storage.clear_all()
        assert result == True

        planes = self.storage.get_all()
        assert len(planes) == 0

    def test_get_by_country(self):
        """Тест поиска по стране"""
        self.storage.add_aeroplane(self.plane1)  # Russia
        self.storage.add_aeroplane(self.plane2)  # USA

        russian_planes = self.storage.get_by_country("Russia")
        assert len(russian_planes) == 1
        assert russian_planes[0].callsign == "TEST1"

    def test_get_top_by_altitude(self):
        """Тест получения топа по высоте"""
        self.storage.add_aeroplane(self.plane1)  # 10000
        self.storage.add_aeroplane(self.plane2)  # 9000

        plane3 = Aeroplane("TEST3", "Germany", altitude=11000)
        self.storage.add_aeroplane(plane3)

        top2 = self.storage.get_top_by_altitude(2)
        assert len(top2) == 2
        assert top2[0].altitude == 11000  # Самая высокая
        assert top2[1].altitude == 10000  # Вторая по высоте