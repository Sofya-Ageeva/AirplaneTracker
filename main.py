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
    print("1. Получить данные о самолетах из API")
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

    print("""
    ╔════════════════════════════════════════════╗
    ║     ✈️  МОНИТОРИНГ САМОЛЕТОВ  ✈️           ║
    ║     Отслеживание воздушных судов           ║
    ╚════════════════════════════════════════════╝
    """)

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

                # Получаем данные
                planes_data = api.get_aeroplanes_by_area(country)

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
                            print(f"Ошибка при создании самолета: {e}")
                            continue

                    print(f"\nНайдено {len(current_aeroplanes)} самолетов!")
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
                    print(f"В {country} не найдено самолетов")

            except Exception as e:
                print(f"Ошибка: {e}")

        # 2. Показать сохраненные самолеты
        elif choice == "2":
            saved_planes = storage.get_all()
            print_aeroplanes(saved_planes, "Сохраненные самолеты")

        # 3. Топ N по высоте
        elif choice == "3":
            # Выбираем источник данных
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
            elif source == "2":
                planes = storage.get_all()
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print("Нет данных")
                continue

            n = input_top_n()
            top_planes = get_top_aeroplanes(planes, n)
            print_aeroplanes(top_planes, f"Топ {n} самолетов по высоте")

        # 4. Фильтрация по стране
        elif choice == "4":
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
            elif source == "2":
                planes = storage.get_all()
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print("Нет данных")
                continue

            countries = input_countries_list()
            if not countries:
                print("Страны не указаны")
                continue

            filtered = filter_by_country(planes, countries)
            print_aeroplanes(filtered, f"Самолеты из стран: {', '.join(countries)}")

        # 5. Фильтрация по высоте
        elif choice == "5":
            source = input("Использовать (1 - текущие, 2 - сохраненные): ").strip()

            if source == "1":
                planes = current_aeroplanes
            elif source == "2":
                planes = storage.get_all()
            else:
                print("Неверный выбор")
                continue

            if not planes:
                print("Нет данных")
                continue

            min_alt, max_alt = input_altitude_range()

            if min_alt is not None and max_alt is not None:
                filtered = filter_by_altitude_range(planes, min_alt, max_alt)
                print_aeroplanes(filtered, f"Самолеты на высоте {min_alt}-{max_alt} м")
            else:
                print_aeroplanes(planes, "Все самолеты")

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
            confirm = input("Очистить все данные? (да/нет): ").strip().lower()
            if confirm in ['да', 'yes', 'y', 'д']:
                if storage.clear_all():
                    print("Хранилище очищено")
                else:
                    print("Ошибка при очистке")

        else:
            print("Неверный выбор")


if __name__ == "__main__":
    main()
