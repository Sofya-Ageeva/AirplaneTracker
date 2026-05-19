from abc import ABC, abstractmethod
from typing import Any, List

from src.aeroplane import Aeroplane


class AbstractStorage(ABC):
    """Абстрактный класс для работы с хранилищем"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Добавление информации о самолете в хранилище"""
        pass

    @abstractmethod
    def get_aeroplanes(self, **criteria: Any) -> List[Aeroplane]:
        """Получение данных из хранилища по критериям"""
        pass

    @abstractmethod
    def delete_aeroplane(self, aeroplane: Aeroplane) -> bool:
        """Удаление информации о самолете"""
        pass

    @abstractmethod
    def update_aeroplane(self, callsign: str, aeroplane: Aeroplane) -> bool:
        """Обновление информации о самолете"""
        pass

    @abstractmethod
    def get_all(self) -> List[Aeroplane]:
        """Получение всех самолетов из хранилища"""
        pass

    @abstractmethod
    def clear_all(self) -> bool:
        """Очистка хранилища"""
        pass
