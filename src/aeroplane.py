from typing import Optional, Dict, Any


class Aeroplane:
    """Класс, представляющий самолет"""

    def __init__(self,
                 callsign: str,
                 origin_country: str,
                 velocity: Optional[float]=None,
                 altitude: Optional[float]=None,
                 icao24: Optional[str]=None,
                 heading: Optional[float]=None,
                 on_ground: Optional[bool]=False) -> None:
        """Создание нового самолета"""
        # Проверяем, что обязательные поля не пустые
        if not callsign:
            raise ValueError("Позывной не может быть пустым")
        if not origin_country:
            raise ValueError("Страна регистрации не может быть пустой")

        self._callsign: str = callsign
        self._origin_country: str = origin_country
        self._velocity: float = velocity if velocity is not None else 0.0
        self._altitude: float = altitude if altitude is not None else 0.0
        self._icao24: str = icao24 if icao24 else ""
        self._heading: float = heading if heading is not None else 0.0
        self._on_ground: bool = on_ground if on_ground is not None else False

        # Проверяем, что скорость и высота не отрицательные
        if self._velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        if self._altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

    # Геттеры - методы для получения значений
    @property
    def callsign(self) -> str:
        """Позывной самолета"""
        return self._callsign

    @property
    def origin_country(self) -> str:
        """Страна регистрации"""
        return self._origin_country

    @property
    def velocity(self) -> float:
        """Скорость в км/ч"""
        return self._velocity

    @property
    def altitude(self) -> float:
        """Высота в метрах"""
        return self._altitude

    @property
    def icao24(self) -> str:
        """ICAO24 идентификатор"""
        return self._icao24

    @property
    def heading(self) -> float:
        """Курс в градусах"""
        return self._heading

    @property
    def on_ground(self) -> bool:
        """Находится ли на земле"""
        return self._on_ground

    def compare_by_velocity(self, other: 'Aeroplane') -> int:
        """Сравнение скорости самолетов"""
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только с объектом Aeroplane")

        if self._velocity > other._velocity:
            return 1
        elif self._velocity < other._velocity:
            return -1
        else:
            return 0

    def compare_by_altitude(self, other: 'Aeroplane') -> int:
        """Сравнение высоты самолетов"""
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только с объектом Aeroplane")

        if self._altitude > other._altitude:
            return 1
        elif self._altitude < other._altitude:
            return -1
        else:
            return 0

    def __str__(self) -> str:
        """Вывод информации о самолете"""
        status = "на земле" if self._on_ground else "в воздухе"
        return (f"✈ {self._callsign} | {self._origin_country} | "
                f"Скорость: {self._velocity} км/ч | Высота: {self._altitude} м | "
                f"Статус: {status}")

    def to_dict(self) -> Dict[str, Any]:
        """Запись данных о самолетах в словарь"""
        return {
            'callsign': self._callsign,
            'origin_country': self._origin_country,
            'velocity': self._velocity,
            'altitude': self._altitude,
            'icao24': self._icao24,
            'heading': self._heading,
            'on_ground': self._on_ground
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Aeroplane':
        """Создает самолет из словаря"""
        return cls(
            callsign=data.get('callsign', ''),
            origin_country=data.get('origin_country', ''),
            velocity=data.get('velocity'),
            altitude=data.get('altitude'),
            icao24=data.get('icao24'),
            heading=data.get('heading'),
            on_ground=data.get('on_ground', False)
        )
