from src.aeroplane import Aeroplane
from src.storage import JSONSaver
from src.api import AeroplanesAPI


def print_aeroplanes(aeroplanes, title="Список самолетов"):
    """Выводит список самолетов в консоль"""
    print(f"\n{'=' * 60}")
    print(f"{title}")
    print(f"{'=' * 60}")

    if not aeroplanes:
        print("Самолеты не найдены")
        return

    for i, plane in enumerate(aeroplanes, 1):
        print(f"{i}. {plane}")

    print(f"\nВсего найдено: {len(aeroplanes)} самолетов")


def get_top_aeroplanes(aeroplanes, n):
    """Возвращает топ N самолетов по высоте из списка"""
    if not aeroplanes:
        return []

    # Сортируем по высоте (от большей к меньшей)
    sorted_planes = sorted(aeroplanes, key=lambda x: x.altitude, reverse=True)
    # Берем первые N
    return sorted_planes[:min(n, len(sorted_planes))]


def filter_by_country(aeroplanes, countries):
    """Фильтрует самолеты по списку стран"""
    if not aeroplanes:
        return []

    result = []
    for plane in aeroplanes:
        if plane.origin_country in countries:
            result.append(plane)

    return result


def filter_by_altitude_range(aeroplanes, min_alt, max_alt):
    """Фильтрует самолеты по диапазону высот"""
    if not aeroplanes:
        return []

    result = []
    for plane in aeroplanes:
        if min_alt <= plane.altitude <= max_alt:
            result.append(plane)

    return result


def input_country():
    """Запрашивает у пользователя название страны"""
    while True:
        country = input("\nВведите название страны (например, Russia, USA, Germany): ").strip()
        if country:
            return country
        print("Название страны не может быть пустым")


def input_top_n():
    """Запрашивает у пользователя число N для топа"""
    while True:
        try:
            n = input("Введите количество самолетов для топа N: ").strip()
            if not n:
                return 10  # Значение по умолчанию

            n_int = int(n)
            if n_int <= 0:
                print("Число должно быть положительным")
                continue

            return n_int
        except ValueError:
            print("Введите целое число")


def input_countries_list():
    """Запрашивает список стран для фильтрации"""
    countries_input = input("Введите страны через пробел: ").strip()
    if not countries_input:
        return []

    return [c.strip() for c in countries_input.split()]


def input_altitude_range():
    """Запрашивает диапазон высот"""
    while True:
        range_input = input("Введите диапазон высот (например, 1000 - 10000) или Enter для пропуска: ").strip()

        if not range_input:
            return None, None

        try:
            parts = range_input.split('-')
            if len(parts) != 2:
                print("Используйте формат: мин - макс")
                continue

            min_alt = float(parts[0].strip())
            max_alt = float(parts[1].strip())

            if min_alt < 0 or max_alt < 0:
                print("Высота не может быть отрицательной")
                continue

            # Если мин больше макс - меняем местами
            if min_alt > max_alt:
                min_alt, max_alt = max_alt, min_alt

            return min_alt, max_alt
        except ValueError:
            print("Введите числа")
