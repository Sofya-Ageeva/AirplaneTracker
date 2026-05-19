from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional


class AbstractAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> Optional[Dict[str, float]]:
        """Получение географических координат страны"""
        pass

    @abstractmethod
    def get_aeroplanes_by_area(self, country_name: str) -> List[Dict[str, Any]]:
        """Получение информации о самолетах в воздушном пространстве страны"""
        pass
