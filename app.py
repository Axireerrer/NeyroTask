import os
import asyncio

from dotenv import load_dotenv, find_dotenv
from functions.geolocation_city import get_geolocation_city
from functions.weather_forecast import get_weather_forecast
from functions.prompt import create_prompt

from requests_api.gigachat_api_gpt import ask_gigachat_api_gpt
from requests_api.yandex_api_gpt import ask_yandex_api_gpt

from files_operations.file_yandex import write_output_in_yandex_file
from files_operations.file_gigachatgpt import write_output_in_gigachat_file

# Загрузка API-ключа и токенов доступа из переменных окружения
load_dotenv(find_dotenv())
api_key = os.getenv('API_KEY')
access_token_gigachat = os.getenv('GIGACHAT_TOKEN')
access_token_yandex = os.getenv('YANDEX_TOKEN')
yandex_client_id = os.getenv('YANDEX_CLIENT_ID')


# Список доступных жанров
list_of_genres = ['Drama', 'Comedy', 'Musical', 'Detective', 'Action', 'Horror']

try:
    # Ввод данных от пользователя
    city_name, genre, length = input("Введите город, жанр, длину создаваемого текста: ").split()

    # Проверка, является ли длина целым числом
    if type(length) == str:
        length = int(length)

    # Проверка, присутствует ли жанр в списке доступных жанров
    if genre not in list_of_genres:
        raise ValueError("You can use only genre as Drama, Comedy, Musical, Detective, Action, Horror")

    # Получение координат города
    coord = get_geolocation_city(city_name=city_name, api_key=api_key)

    # Получение прогноза погоды
    weather_tomorrow = get_weather_forecast(api_key=api_key, lat=coord[0], lon=coord[1])
    # Получение промпта, т.е. запроса для нейросети
    prompt = create_prompt(city_name=city_name, genre=genre, length=length, weather_tomorrow=weather_tomorrow)
    # Работа GIGACHAT_GPT_API

    async def main():
        gigachat_info = await ask_gigachat_api_gpt(prompt=prompt, access_token=access_token_gigachat)
        yandex_info = await ask_yandex_api_gpt(access_token=access_token_yandex, client_id=yandex_client_id, prompt=prompt)

        await write_output_in_yandex_file(yandex_info)
        await write_output_in_gigachat_file(gigachat_info)
        print("\tВремя работы GIGACHAT_GPT_API: ", gigachat_info['during_request_gigachat'])
        print()
        print("\tВремя работы YANDEX_GPT_API: ", yandex_info['during_request_yandexgptapi'])

    # Создание и вывод запроса
    if __name__ == '__main__':
        print(prompt)
        print()
        asyncio.run(main())

except Exception as e:
    print(f"An error occurred: {e}")