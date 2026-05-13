import pytest
from src.aeroplane import Aeroplane


class TestAeroplane:
    """Тесты для самолета"""

    def test_create_aeroplane(self):
        """Тест создания самолета"""
        plane = Aeroplane("AFL123", "Russia", 850, 10000)

        assert plane.callsign == "AFL123"
        assert plane.origin_country == "Russia"
        assert plane.velocity == 850
        assert plane.altitude == 10000

    def test_create_with_default_values(self):
        """Тест создания с значениями по умолчанию"""
        plane = Aeroplane("TEST", "Test Country")

        assert plane.velocity == 0
        assert plane.altitude == 0
        assert plane.on_ground == False

    def test_invalid_callsign(self):
        """Тест: пустой позывной"""
        with pytest.raises(ValueError):
            Aeroplane("", "Russia")

    def test_invalid_country(self):
        """Тест: пустая страна"""
        with pytest.raises(ValueError):
            Aeroplane("AFL123", "")

    def test_negative_velocity(self):
        """Тест: отрицательная скорость"""
        with pytest.raises(ValueError):
            Aeroplane("AFL123", "Russia", velocity=-100)

    def test_negative_altitude(self):
        """Тест: отрицательная высота"""
        with pytest.raises(ValueError):
            Aeroplane("AFL123", "Russia", altitude=-500)

    def test_compare_by_velocity(self):
        """Тест сравнения по скорости"""
        plane1 = Aeroplane("A", "Rus", velocity=800)
        plane2 = Aeroplane("B", "Rus", velocity=700)
        plane3 = Aeroplane("C", "Rus", velocity=800)

        assert plane1.compare_by_velocity(plane2) == 1  # plane1 быстрее
        assert plane2.compare_by_velocity(plane1) == -1  # plane2 медленнее
        assert plane1.compare_by_velocity(plane3) == 0  # равны

    def test_compare_by_altitude(self):
        """Тест сравнения по высоте"""
        plane1 = Aeroplane("A", "Rus", altitude=10000)
        plane2 = Aeroplane("B", "Rus", altitude=8000)
        plane3 = Aeroplane("C", "Rus", altitude=10000)

        assert plane1.compare_by_altitude(plane2) == 1  # plane1 выше
        assert plane2.compare_by_altitude(plane1) == -1  # plane2 ниже
        assert plane1.compare_by_altitude(plane3) == 0  # равны

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        plane = Aeroplane("AFL123", "Russia", 850, 10000)
        plane_dict = plane.to_dict()

        assert plane_dict['callsign'] == "AFL123"
        assert plane_dict['origin_country'] == "Russia"
        assert plane_dict['velocity'] == 850
        assert plane_dict['altitude'] == 10000

    def test_from_dict(self):
        """Тест создания из словаря"""
        data = {
            'callsign': 'AFL123',
            'origin_country': 'Russia',
            'velocity': 850,
            'altitude': 10000,
            'icao24': '123ABC',
            'heading': 180,
            'on_ground': False
        }

        plane = Aeroplane.from_dict(data)

        assert plane.callsign == "AFL123"
        assert plane.origin_country == "Russia"
        assert plane.velocity == 850
        assert plane.altitude == 10000

    def test_string_representation(self):
        """Тест строкового представления"""
        plane = Aeroplane("AFL123", "Russia", 850, 10000)
        plane_str = str(plane)

        assert "AFL123" in plane_str
        assert "Russia" in plane_str
        assert "850" in plane_str
        assert "10000" in plane_str