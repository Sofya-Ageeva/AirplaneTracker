import json
import os
from src.aeroplane import Aeroplane


class JSONSaver:
    """Класс для сохранения самолетов в JSON файл"""

    def __init__(self, filename="data/aeroplanes.json"):
        """Создание хранилища"""
        self.filename = filename
        # Создаем папку, если её нет
        self.ensure_directory_exists()
        # Создаем файл, если его нет
        self.ensure_file_exists()


    def ensure_directory_exists(self):
        """Создает папку для файла, если её нет"""
        directory = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)


    def ensure_file_exists(self):
        """Создает пустой JSON файл, если его нет"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_data(self):
        """Загружает данные из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

    def save_data(self, data):
        """Сохраняет данные в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

    def add_aeroplane(self, aeroplane):
        """Добавляет самолет в хранилище"""
        # Загружаем существующие данные
        data = self.load_data()

        # Получаем словарь с данными самолета
        aeroplane_dict = aeroplane.to_dict()

        # Проверяем, нет ли уже такого самолета (по ICAO24)
        for existing in data:
            if existing.get('icao24') == aeroplane_dict['icao24']:
                print(f"  Самолет {aeroplane.callsign} уже есть в файле")
                return False

        # Добавляем новый самолет
        data.append(aeroplane_dict)

        # Сохраняем обратно
        return self.save_data(data)

    def get_all(self):
        """
        Получает все самолеты из хранилища

        Возвращает:
            Список объектов Aeroplane
        """
        data = self.load_data()
        aeroplanes = []

        for item in data:
            try:
                aeroplane = Aeroplane.from_dict(item)
                aeroplanes.append(aeroplane)
            except Exception as e:
                print(f"  Ошибка при загрузке самолета: {e}")
                continue

        return aeroplanes

    def delete_aeroplane(self, aeroplane):
        """Удаляет самолет из хранилища"""
        data = self.load_data()
        initial_count = len(data)

        # Оставляем только те самолеты, у которых другой ICAO24
        data = [item for item in data if item.get('icao24') != aeroplane.icao24]

        if len(data) < initial_count:
            return self.save_data(data)
        return False

    def clear_all(self):
        """Очищает все данные в хранилище"""
        return self.save_data([])

    def get_by_country(self, country):
        """Получает самолеты по стране регистрации"""
        all_planes = self.get_all()
        return [p for p in all_planes if p.origin_country == country]

    def get_top_by_altitude(self, n):
        """Получает топ N самолетов по высоте"""
        all_planes = self.get_all()
        # Сортируем по высоте (от большей к меньшей)
        all_planes.sort(key=lambda x: x.altitude, reverse=True)
        # Возвращаем первые N
        return all_planes[:n]
