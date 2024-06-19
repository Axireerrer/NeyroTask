

def create_prompt(city_name: str, genre: str, length: int, weather_tomorrow: dict) -> str:

    """
        Создает текстовый запрос для написания сказки на основе данных о погоде.

        Параметры:
        city_name (str): Название города.
        genre (str): Жанр сказки.
        length (int): Максимальная длина сказки в символах.
        weather_tomorrow (dict): Словарь с описанием погоды на завтра, содержащий ключи 'description' и 'temperature'.

        Возвращает:
        str: Текстовый запрос для написания сказки.

        Пример использования:
        >>> weather = {'description': 'ясно', 'temperature': 25}
        >>> create_prompt("Москва", "фэнтези", 500, weather)
        '\n\tПридумай сказку в жанре фэнтези про погоду в городе Москва на завтра.\n\tПогода: ясно, температура: 25 градусов.\n\tДлина не более 500 символов.'
        """
    weather_description = weather_tomorrow['description']
    weather_temperature = weather_tomorrow['temperature']

    prompt = (f'\n\tПридумай сказку в жанре {genre} про погоду в городе {city_name} на завтра.'
    f'\n\tПогода: {weather_description}, температура: {weather_temperature} градусов.'
    f'\n\tДлина не более {length} символов.')

    return prompt
