from src.api import AeroplanesAPI
from src.aeroplane import Aeroplane
from src.storage import JSONSaver
from src.utils import (
    print_aeroplanes, get_top_aeroplanes, filter_by_country,
    filter_by_altitude_range, input_country, input_top_n,
    input_countries_list, input_altitude_range
)


def show_menu():
    """Показывает главное меню"""
    print("\n" + "=" * 60)
    print("ГЛАВНОЕ МЕНЮ:")
    print("1. Получить данные о самолетах")
    print("2. Показать сохраненные самолеты")
    print("3. Топ N самолетов по высоте")
    print("4. Фильтрация по стране регистрации")
    print("5. Фильтрация по диапазону высот")
    print("6. Сохранить текущие данные в файл")
    print("7. Очистить хранилище")
    print("0. Выход")
    print("=" * 60)


def main():
    """Главная функция программы"""

    print("""МОНИТОРИНГ САМОЛЕТОВ""")

    # Создаем объекты для работы
    api = None
    current_aeroplanes = []  # Текущие данные из API
    storage = JSONSaver()  # Хранилище в файле

    while True:
        show_menu()
        choice = input("Выберите действие (0-7): ").strip()

        # Выход из программы
        if choice == "0":
            print("\nДо свидания!")
            break

        # 1. Получить данные из API
        elif choice == "1":
            try:
                country = input_country()
                print(f"\nПолучение данных о самолетах в {country}...")

                # Создаем объект API
                api = AeroplanesAPI()

                # Пробуем разные варианты названий для некоторых стран
                countries_to_try = [country]

                # Добавляем альтернативные названия для популярных стран
                country_alternatives = {
                    'usa': ['United States', 'USA', 'United States of America'],
                    'russia': ['Russia', 'Russian Federation'],
                    'uk': ['United Kingdom', 'UK', 'Great Britain'],
                    'germany': ['Germany', 'Deutschland'],
                    'france': ['France', 'French Republic'],
                    'spain': ['Spain', 'España'],
                    'italy': ['Italy', 'Italia'],
                    'china': ['China', 'People\'s Republic of China'],
                }

                # Проверяем, есть ли альтернативы для введенной страны
                for key, alternatives in country_alternatives.items():
                    if country.lower() == key or country.lower() in [a.lower() for a in alternatives]:
                        countries_to_try = alternatives
                        break

                planes_data = []
                last_error = None

                # Пробуем каждый вариант названия
                for try_country in countries_to_try:
                    try:
                        print(f"  Пробуем: {try_country}")
                        planes_data = api.get_aeroplanes_by_area(try_country)
                        if planes_data:
                            print(f"  ✓ Успешно! Использовано название: {try_country}")
                            break
                    except Exception as e:
                        last_error = e
                        continue

                if not planes_data and last_error:
                    raise last_error

                if planes_data:
                    # Преобразуем словари в объекты Aeroplane
                    current_aeroplanes = []
                    for data in planes_data:
                        try:
                            plane = Aeroplane(
                                callsign=data.get('callsign', ''),
                                origin_country=data.get('origin_country', ''),
                                velocity=data.get('velocity'),
                                altitude=data.get('altitude'),
                                icao24=data.get('icao24'),
                                heading=data.get('heading'),
                                on_ground=data.get('on_ground', False)
                            )
                            current_aeroplanes.append(plane)
                        except Exception as e:
                            print(f"  Предупреждение: не удалось создать самолет: {e}")
                            continue

                    print(f"\nНайдено {len(current_aeroplanes)} самолетов!")

                    if current_aeroplanes:
                        print_aeroplanes(current_aeroplanes, f"Самолеты в {country}")

                        # Спрашиваем, сохранить ли
                        save = input("\nСохранить в файл? (да/нет): ").strip().lower()
                        if save in ['да', 'yes', 'y', 'д']:
                            saved = 0
                            for plane in current_aeroplanes:
                                if storage.add_aeroplane(plane):
                                    saved += 1
                            print(f"Сохранено {saved} самолетов")
                    else:
                        print(f"В {country} найдены записи, но все без позывных")
                else:
                    print(f"В {country} не найдено самолетов")

            except Exception as e:
                print(f"\nОшибка: {e}")
                print("\nСоветы:")
                print("  - Попробуйте использовать полное название страны (например, 'United States' вместо 'USA')")
                print("  - Проверьте подключение к интернету")
                print("  - Некоторые страны могут быть недоступны в API")

        # 2. Показать сохраненные самолеты
        elif choice == "2":
            saved_planes = storage.get_all()
            if saved_planes:
                print_aeroplanes(saved_planes, "Сохраненные самолеты")
            else:
                print("\nВ хранилище пока нет самолетов. Сначала получите данные (пункт 1)")

        # 3. Топ N по высоте
        elif choice == "3":
            # Выбираем источник данных
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
                source_name = "текущих"
            elif source == "2":
                planes = storage.get_all()
                source_name = "сохраненных"
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print(f"Нет {source_name} данных")
                continue

            n = input_top_n()
            top_planes = get_top_aeroplanes(planes, n)
            print_aeroplanes(top_planes, f"Топ {n} самолетов по высоте из {source_name} данных")

        # 4. Фильтрация по стране
        elif choice == "4":
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
                source_name = "текущих"
            elif source == "2":
                planes = storage.get_all()
                source_name = "сохраненных"
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print(f"Нет {source_name} данных")
                continue

            countries = input_countries_list()
            if not countries:
                print("Страны не указаны")
                continue

            filtered = filter_by_country(planes, countries)
            print_aeroplanes(filtered, f"Самолеты из стран: {', '.join(countries)} ({source_name} данные)")

        # 5. Фильтрация по высоте
        elif choice == "5":
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
                source_name = "текущих"
            elif source == "2":
                planes = storage.get_all()
                source_name = "сохраненных"
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print(f"Нет {source_name} данных")
                continue

            min_alt, max_alt = input_altitude_range()

            if min_alt is not None and max_alt is not None:
                filtered = filter_by_altitude_range(planes, min_alt, max_alt)
                print_aeroplanes(filtered, f"Самолеты на высоте {min_alt}-{max_alt} м ({source_name} данные)")
            else:
                print_aeroplanes(planes, f"Все самолеты ({source_name} данные)")

        # 6. Сохранить текущие данные
        elif choice == "6":
            if not current_aeroplanes:
                print("Текущие данные отсутствуют")
                continue

            saved = 0
            for plane in current_aeroplanes:
                if storage.add_aeroplane(plane):
                    saved += 1
            print(f"Сохранено {saved} из {len(current_aeroplanes)} самолетов")

        # 7. Очистить хранилище
        elif choice == "7":
            saved_planes = storage.get_all()
            if not saved_planes:
                print("Хранилище уже пустое")
                continue

            confirm = input(f"Удаление {len(saved_planes)} самолетов. (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y', 'д']:
                if storage.clear_all():
                    print("Хранилище очищено")
                else:
                    print("Ошибка при очистке")

        else:
            print("Неверный выбор. Введите число от 0 до 7")


if __name__ == "__main__":
    main()