import aiohttp
import json
import time


async def ask_gigachat_api_gpt(access_token: str, prompt: str) -> dict:
    """
       Отправляет запрос к API GigaChat с использованием заданного токена доступа и запроса,
       и возвращает ответ API.

       Параметры:
       access_token (str): Токен доступа для аутентификации запроса.
       prompt (str): Текст запроса, который будет отправлен модели GigaChat.

       Возвращает:
       dict: Словарь, содержащий время выполнения запроса ('during_request_gigachat') и
             текстовый ответ API ('text').
       """

    # URL для API GigaChat
    url = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

    # Создание payload с параметрами для запроса
    payload = json.dumps({
        "model": "GigaChat",
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
        "temperature": 1,
        "top_p": 0.1,
        "n": 1,
        "stream": False,
        "max_tokens": 512,
        "repetition_penalty": 1
    })

    # Заголовки для запроса
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': f'Bearer {access_token}',
    }

    # Создание асинхронной сессии для отправки запроса
    async with aiohttp.ClientSession() as session:
        start = time.time()

        # Отправка POST запроса к API GigaChat
        async with session.post(url, headers=headers, data=payload, ssl=False) as response:

            # Проверка статуса ответа
            if response.status != 200:
                error_message = await response.json()
                print(f"An error occurred: {error_message}")
                return {'error': error_message}

            response_text = await response.json()
            end = time.time()

            # Вычисление времени выполнения запроса
            during_request_gigachat = float(end - start)
            print("\tВремя работы GIGACHAT_GPT_API: ", during_request_gigachat)

            # Формирование данных для возврата
            data = {
                'text': response_text,
            }
            return data


