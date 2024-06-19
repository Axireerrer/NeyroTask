import requests


def get_weather_forecast(api_key: str, lat: float, lon: float) -> dict:

    """
      Получает прогноз погоды для указанной географической широты и долготы с помощью API OpenWeatherMap.

      Параметры:
      api_key (str): API-ключ для доступа к OpenWeatherMap.
      lat (float): Широта местоположения.
      lon (float): Долгота местоположения.

      Возвращает:
      dict: Словарь с описанием погоды и температурой.

      Исключения:
      ValueError: Если данные о погоде не найдены.
      requests_api.exceptions.ConnectionError: Если произошла ошибка соединения.

      Пример использования:
      >>> get_weather_forecast("api_key", 51.5074, -0.1278)
      {'description': 'clear sky', 'temperature': 15}
      """
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            weather_tomorrow = {
                'description': data['weather'][0]['description'],
                'temperature': int((data['main']['temp'] - 273)),  # Конвертация из Фаренгейта в Цельсий
            }
            return weather_tomorrow
        else:
            raise ValueError("No weather data found for the given coordinates.")
    except requests.exceptions.ConnectionError as conn_err:
        print(f"Connection error occurred: {conn_err}")



