import requests
import os


class AeroplanesAPI:
    """Класс для получения данных о самолетах через API"""

    def __init__(self):
        # Адреса API сервисов
        self.nominatim_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        # Таймаут для запросов (в секундах)
        self.timeout = 20
        user_email = os.environ.get('AIRPLANE_TRACKER_EMAIL')
        self.headers = {
            'User-Agent': f'AirplaneTracker/1.0 ({user_email})',
            'Accept': 'application/json'
        }

    def get_country_coordinates(self, country_name):
        """Получает координаты страны через Nominatim API"""
        try:
            # Параметры запроса
            params = {
                'q': country_name,  # Название страны
                'format': 'json',  # Ответ в формате JSON
                'limit': 1  # Берем только первый результат
            }

            # Отправляем GET запрос с правильными заголовками
            print(f"  Запрос координат страны {country_name}...")
            response = requests.get(
                self.nominatim_url,
                params=params,
                headers=self.headers,  # Добавляем заголовки!
                timeout=self.timeout
            )

            # Проверяем, что запрос успешен
            response.raise_for_status()

            # Получаем данные
            data = response.json()

            # Если страна найдена
            if data and len(data) > 0:
                bounding_box = data[0].get('boundingbox', [])
                if bounding_box and len(bounding_box) >= 4:
                    # Nominatim возвращает строки, преобразуем в числа
                    south = float(bounding_box[0])
                    north = float(bounding_box[1])
                    west = float(bounding_box[2])
                    east = float(bounding_box[3])

                    print(f"Найдены координаты: {south}°S, {north}°N, {west}°W, {east}°E")

                    return {
                        'south': south,
                        'north': north,
                        'west': west,
                        'east': east
                    }

            # Если страна не найдена
            raise ValueError(f"Страна '{country_name}' не найдена")

        except requests.Timeout:
            raise Exception("Превышено время ожидания при запросе координат. Попробуйте еще раз.")
        except requests.HTTPError as e:
            if e.response.status_code == 403:
                raise Exception("Ошибка доступа к API. Попробуйте использовать другое название страны.")
            else:
                raise Exception(f"HTTP ошибка {e.response.status_code}: {e}")
        except requests.RequestException as e:
            raise Exception(f"Ошибка подключения: {e}")
        except ValueError as e:
            raise Exception(str(e))
        except Exception as e:
            raise Exception(f"Неожиданная ошибка: {e}")

    def get_aeroplanes_by_area(self, country_name):
        """Получает список самолетов в воздушном пространстве страны"""
        try:
            # 1. Получаем координаты страны
            coordinates = self.get_country_coordinates(country_name)

            print(f"  Координаты получены, запрашиваем самолеты...")

            # 2. Формируем запрос к OpenSky API
            params = {
                'lamin': coordinates['south'],  # Южная граница
                'lamax': coordinates['north'],  # Северная граница
                'lomin': coordinates['west'],  # Западная граница
                'lomax': coordinates['east']  # Восточная граница
            }

            # 3. Отправляем запрос к OpenSky
            # OpenSky не требует специального User-Agent
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
                    print(f"  Найдено {len(states)} записей, обрабатываем...")

                    for state in states:
                        # Проверяем, что данные есть
                        if state and len(state) >= 10:
                            # Очищаем позывной от пробелов
                            callsign = state[1].strip() if state[1] else ""

                            # Создаем словарь с информацией о самолете
                            aeroplane = {
                                'icao24': state[0],  # Уникальный код
                                'callsign': callsign,  # Позывной
                                'origin_country': state[2],  # Страна регистрации
                                'longitude': state[5],  # Долгота
                                'latitude': state[6],  # Широта
                                'altitude': state[7],  # Высота (м)
                                'velocity': state[9],  # Скорость (м/с)
                                'heading': state[10],  # Курс
                                'on_ground': state[8]  # На земле?
                            }

                            # Пропускаем самолеты без позывного
                            if callsign and aeroplane['origin_country']:
                                # Конвертируем скорость из м/с в км/ч
                                if aeroplane['velocity']:
                                    aeroplane['velocity'] = round(aeroplane['velocity'] * 3.6, 2)

                                aeroplanes.append(aeroplane)

                    print(f"Обработано {len(aeroplanes)} самолетов с позывными")
                else:
                    print(f"В воздушном пространстве {country_name} нет самолетов")
            else:
                print(f"Не удалось получить данные от OpenSky API")

            return aeroplanes

        except Exception as e:
            raise Exception(f"Ошибка при получении данных о самолетах: {e}")
