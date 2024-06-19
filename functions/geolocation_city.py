import requests


def get_geolocation_city(city_name: str, api_key: str) -> tuple:

    """
        Получает географические координаты (широту и долготу) города
        по его названию с помощью API OpenWeatherMap.

        Параметры:
        city_name (str): Название города.
        api_key (str): API-ключ для доступа к OpenWeatherMap.

        Возвращает:
        tuple: Кортеж, содержащий широту и долготу города.

        Исключения:
        ValueError: Если данные для указанного города не найдены.
        requests_api.exceptions.ConnectionError: Если произошла ошибка соединения.

        Пример использования:
        >>> get_geolocation_city("London", "api_key")
        (51.5074, -0.1278)
        """

    url = f"http://api.openweathermap.org/geo/1.0/direct?q={city_name}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            lat = data[0]['lat']
            lon = data[0]['lon']
            coord = lat, lon
            return coord
        else:
            raise ValueError("No data found for the given city.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")





