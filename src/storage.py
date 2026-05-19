import json
import os
from typing import Any, Dict, List

from src.abstract_storage import AbstractStorage
from src.aeroplane import Aeroplane


class JSONSaver(AbstractStorage):
    """Класс для сохранения самолетов в JSON файл"""

    def __init__(self, filename: str = "data/aeroplanes.json") -> None:
        """Создание хранилища"""
        self.filename: str = filename
        # Создаем папку, если её нет
        self.ensure_directory_exists()
        # Создаем файл, если его нет
        self.ensure_file_exists()

    def ensure_directory_exists(self) -> None:
        """Создает папку для файла, если её нет"""
        directory: str = os.path.dirname(self.filename)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)

    def ensure_file_exists(self) -> None:
        """Создает пустой JSON файл, если его нет"""
        if not os.path.exists(self.filename):
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def load_data(self) -> List[Dict[str, Any]]:
        """Загружает данные из файла"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                data: List[Dict[str, Any]] = json.load(f)
                return data
        except (json.JSONDecodeError, FileNotFoundError, IOError):
            return []

    def save_data(self, data: List[Dict[str, Any]]) -> bool:
        """Сохраняет данные в файл"""
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except (IOError, OSError) as e:
            print(f"Ошибка при сохранении файла: {e}")
            return False

    def add_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Добавляет самолет в хранилище"""
        # Загружаем существующие данные
        data: List[Dict[str, Any]] = self.load_data()

        # Получаем словарь с данными самолета
        aeroplane_dict: Dict[str, Any] = aeroplane.to_dict()

        # Проверяем, нет ли уже такого самолета (по ICAO24)
        for existing in data:
            if existing.get('icao24') == aeroplane_dict['icao24']:
                print(f"  Самолет {aeroplane.callsign} уже есть в файле")
                return False

        # Добавляем новый самолет
        data.append(aeroplane_dict)

        # Сохраняем обратно
        return self.save_data(data)

    def get_all(self) -> List[Aeroplane]:
        """Получает все самолеты из хранилища"""
        data: List[Dict[str, Any]] = self.load_data()
        aeroplanes: List[Aeroplane] = []

        for item in data:
            try:
                aeroplane = Aeroplane.from_dict(item)
                aeroplanes.append(aeroplane)
            except Exception as e:
                print(f"  Ошибка при загрузке самолета: {e}")
                continue

        return aeroplanes

    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Удаляет самолет из хранилища"""
        data: List[Dict[str, Any]] = self.load_data()
        initial_count: int = len(data)

        # Оставляем только те самолеты, у которых другой ICAO24
        data = [item for item in data if item.get('icao24') != aeroplane.icao24]

        if len(data) < initial_count:
            return self.save_data(data)
        return False

    def clear_all(self) -> bool:
        """Очищает все данные в хранилище"""
        return self.save_data([])

    def get_by_country(self, country: str) -> List[Aeroplane]:
        """Получает самолеты по стране регистрации"""
        all_planes: List[Aeroplane] = self.get_all()
        return [p for p in all_planes if p.origin_country == country]

    def get_top_by_altitude(self, n: int) -> List[Aeroplane]:
        """Получает топ N самолетов по высоте"""
        all_planes = self.get_all()
        # Сортируем по высоте (от большей к меньшей)
        all_planes.sort(key=lambda x: x.altitude, reverse=True)
        # Возвращаем первые N
        return all_planes[:n]

    def update_aeroplane(self, callsign: str, aeroplane: Aeroplane) -> bool:
        """Обновляет информацию о самолете"""
        data: List[Dict[str, Any]] = self.load_data()

        for i, item in enumerate(data):
            if item.get('callsign') == callsign:
                data[i] = aeroplane.to_dict()
                return self.save_data(data)

        print(f"Самолет с позывным {callsign} не найден")
        return False

    def get_aeroplanes(self, **criteria: Any) -> List[Aeroplane]:
        """Получает самолеты по критериям"""
        data: List[Dict[str, Any]] = self.load_data()
        aeroplanes: List[Aeroplane] = []

        for item in data:
            match: bool = True
            for key, value in criteria.items():
                if key in item and item[key] != value:
                    match = False
                    break

            if match:
                try:
                    aeroplane: Aeroplane = Aeroplane.from_dict(item)
                    aeroplanes.append(aeroplane)
                except (ValueError, TypeError) as e:
                    print(f"Ошибка при создании самолета: {e}")
                    continue

        return aeroplanes
