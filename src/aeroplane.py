class Aeroplane:
    """Класс, представляющий самолет"""

    def __init__(self, callsign, origin_country, velocity=None, altitude=None,
                 icao24=None, heading=None, on_ground=False):
        """Создание нового самолета"""
        # Проверяем, что обязательные поля не пустые
        if not callsign:
            raise ValueError("Позывной не может быть пустым")
        if not origin_country:
            raise ValueError("Страна регистрации не может быть пустой")

        # Сохраняем данные (с нижним подчеркиванием - значит "приватные")
        self._callsign = callsign
        self._origin_country = origin_country
        self._velocity = velocity if velocity is not None else 0.0
        self._altitude = altitude if altitude is not None else 0.0
        self._icao24 = icao24 if icao24 else ""
        self._heading = heading if heading is not None else 0.0
        self._on_ground = on_ground

        # Проверяем, что скорость и высота не отрицательные
        if self._velocity < 0:
            raise ValueError("Скорость не может быть отрицательной")
        if self._altitude < 0:
            raise ValueError("Высота не может быть отрицательной")

    # Геттеры - методы для получения значений
    @property
    def callsign(self):
        """Позывной самолета"""
        return self._callsign

    @property
    def origin_country(self):
        """Страна регистрации"""
        return self._origin_country

    @property
    def velocity(self):
        """Скорость в км/ч"""
        return self._velocity

    @property
    def altitude(self):
        """Высота в метрах"""
        return self._altitude

    @property
    def icao24(self):
        """ICAO24 идентификатор"""
        return self._icao24

    @property
    def heading(self):
        """Курс в градусах"""
        return self._heading

    @property
    def on_ground(self):
        """Находится ли на земле"""
        return self._on_ground

    def compare_by_velocity(self, other):
        """
        Сравнивает два самолета по скорости

        Возвращает:
            1 - если текущий самолет быстрее
            -1 - если текущий самолет медленнее
            0 - если скорости равны
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только с объектом Aeroplane")

        if self._velocity > other._velocity:
            return 1
        elif self._velocity < other._velocity:
            return -1
        else:
            return 0

    def compare_by_altitude(self, other):
        """
        Сравнивает два самолета по высоте

        Возвращает:
            1 - если текущий самолет выше
            -1 - если текущий самолет ниже
            0 - если высоты равны
        """
        if not isinstance(other, Aeroplane):
            raise TypeError("Можно сравнивать только с объектом Aeroplane")

        if self._altitude > other._altitude:
            return 1
        elif self._altitude < other._altitude:
            return -1
        else:
            return 0

    def __str__(self):
        """Красивый вывод информации о самолете"""
        status = "на земле" if self._on_ground else "в воздухе"
        return (f"✈ {self._callsign} | {self._origin_country} | "
                f"Скорость: {self._velocity} км/ч | Высота: {self._altitude} м | "
                f"Статус: {status}")

    def to_dict(self):
        """Превращает самолет в словарь (для сохранения в JSON)"""
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
    def from_dict(cls, data):
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