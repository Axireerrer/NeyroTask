import os
import asyncio

from dotenv import load_dotenv, find_dotenv
from functions.geolocation_city import get_geolocation_city
from functions.weather_forecast import get_weather_forecast
from functions.prompt import create_prompt

from requests_api.gigachat_api_gpt import ask_gigachat_api_gpt
from requests_api.yandex_api_gpt import ask_yandex_api_gpt

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
    gigachat_info = asyncio.run(ask_gigachat_api_gpt(prompt=prompt, access_token=access_token_gigachat))
    # Работа YANDEX_GPT_API

    # yandex_info = asyncio.run(ask_yandex_api_gpt(access_token=access_token_yandex, client_id=yandex_client_id, prompt=prompt))

    # Запись ответа на запрос от нейросети GIGACHAT в файл gigachat.txt
    with open("gigachat.txt", 'w', encoding='utf-8') as file:
        file.write(gigachat_info['text']["choices"][0]["message"]["content"])

    # Запись ответа на запрос от нейросети YANDEX в файл yandexgpt.txt

    # with open("yandexgpt.txt", 'w', encoding='utf-8') as file:
    #     file.write(yandex_info['text']['result']['alternatives'][0]['text'])

    # Создание и вывод запроса
    if __name__ == '__main__':
        print(prompt)
        print()
        print("\tВремя работы GIGACHAT_GPT_API: ", gigachat_info['during_request_gigachat'])
        print()
        # print("\tВремя работы YANDEX_GPT_API: ", yandex_info['during_request_gigachat'])

except Exception as e:
    print(f"An error occurred: {e}")