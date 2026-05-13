import requests


class AeroplanesAPI:
    """Класс для получения данных о самолетах через API"""

    def __init__(self):
        # Адреса API сервисов
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        # Таймаут для запросов (в секундах)
        self.timeout = 10

    def get_country_coordinates(self, country_name):
        """
        Получает координаты страны через Nominatim API

        Аргументы:
            country_name: название страны (например, "Russia")

        Возвращает:
            Словарь с координатами: юг, север, запад, восток
        """
        try:
            # Параметры запроса
            params = {
                'q': country_name,  # Название страны
                'format': 'json',  # Ответ в формате JSON
                'limit': 1  # Берем только первый результат
            }

            # Отправляем GET запрос
            print(f"  Запрос координат страны {country_name}...")
            response = requests.get(
                self.nominatim_url,
                params=params,
                timeout=self.timeout
            )

            # Проверяем, что запрос успешен
            response.raise_for_status()

            # Получаем данные
            data = response.json()

            # Если страна найдена
            if data and len(data) > 0:
                bounding_box = data[0].get('boundingbox', [])
                if bounding_box:
                    return {
                        'south': float(bounding_box[0]),  # Южная граница
                        'north': float(bounding_box[1]),  # Северная граница
                        'west': float(bounding_box[2]),  # Западная граница
                        'east': float(bounding_box[3])  # Восточная граница
                    }

            # Если страна не найдена
            raise ValueError(f"Страна '{country_name}' не найдена")

        except requests.Timeout:
            raise Exception(f"Превышено время ожидания при запросе координат")
        except requests.RequestException as e:
            raise Exception(f"Ошибка при запросе координат: {e}")


    def get_aeroplanes_by_area(self, country_name):
        """Получает список самолетов в воздушном пространстве страны"""
        try:
            # 1. Получаем координаты страны
            coordinates = self.get_country_coordinates(country_name)

            # 2. Формируем запрос к OpenSky API
            params = {
                'lamin': coordinates['south'],  # Южная граница
                'lamax': coordinates['north'],  # Северная граница
                'lomin': coordinates['west'],  # Западная граница
                'lomax': coordinates['east']  # Восточная граница
            }

            # 3. Отправляем запрос к OpenSky
            print(f"  Запрос данных о самолетах...")
            response = requests.get(
                self.opensky_url,
                params=params,
                timeout=self.timeout
            )
            response.raise_for_status()

            # 4. Получаем данные
            data = response.json()

            # 5. Обрабатываем данные
            aeroplanes = []
            if data and 'states' in data:
                states = data['states']
                if states:
                    for state in states:
                        # Проверяем, что данные есть
                        if state and len(state) >= 10:
                            # Создаем словарь с информацией о самолете
                            aeroplane = {
                                'icao24': state[0],  # Уникальный код
                                'callsign': state[1],  # Позывной
                                'origin_country': state[2],  # Страна регистрации
                                'longitude': state[5],  # Долгота
                                'latitude': state[6],  # Широта
                                'altitude': state[7],  # Высота (м)
                                'velocity': state[9],  # Скорость (м/с)
                                'heading': state[10],  # Курс
                                'on_ground': state[8]  # На земле?
                            }

                            # Пропускаем самолеты без позывного
                            if aeroplane['callsign'] and aeroplane['origin_country']:
                                # Конвертируем скорость из м/с в км/ч
                                if aeroplane['velocity']:
                                    aeroplane['velocity'] = round(aeroplane['velocity'] * 3.6, 2)

                                aeroplanes.append(aeroplane)

            return aeroplanes

        except Exception as e:
            raise Exception(f"Ошибка при получении данных о самолетах: {e}")