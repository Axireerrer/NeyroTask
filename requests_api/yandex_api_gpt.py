import json
import time
import aiohttp


async def ask_yandex_api_gpt(prompt: str, access_token: str, client_id: str) -> dict:
    """
      Функция для обращения к Yandex GPT API с заданным промптом и получения ответа.

      :param prompt: Строка с текстом запроса, который будет отправлен в API.
      :param access_token: Токен доступа для аутентификации в API.
      :param client_id: Идентификатор клиента, используемый для доступа к модели.
      :return: Словарь с временем выполнения запроса и текстом ответа или сообщением об ошибке.
      """

    # URL для обращения к Yandex GPT API
    url = "https://llm.api.cloud.yandex.net/foundationModels/v1/completion"

    # Формирование payload в формате JSON
    payload = json.dumps(
        {
            "modelUri": f"gpt://{client_id}/yandexgpt/latest",
            "completionOptions": {
                "stream": False,
                "temperature": 0.3,
                "maxTokens": "1000"
            },
            "messages": [
                {
                    "role": "system",
                    "text": prompt,
                },
            ]
        }
    )

    # Заголовки для запроса
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'x-folder-id': client_id,
    }

    # Создание сессии aiohttp
    async with aiohttp.ClientSession() as session:
        start = time.time()

        # Выполнение POST запроса к API
        async with session.post(url=url, data=payload, headers=headers) as response:

            # Проверка статуса ответа
            if response.status != 200:
                error_message = await response.json()
                print(f"An error occurred: {error_message}")
                return {'error': error_message}

            response_text = await response.json()
            end = time.time()

            # Расчет времени выполнения запроса
            during_request_gigachat = float(end - start)

            # Формирование данных для возврата
            data = {
                'during_request_gigachat': during_request_gigachat,
                'text': response_text,
            }
            print("Full response from API:", response_text)
            return data
