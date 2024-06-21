async def write_output_in_yandex_file(yandex_info):
    # Запись ответа на запрос от нейросети YANDEX в файл yandexgpt.txt
    with open("yandexgpt.txt", 'w', encoding='utf-8') as file:
        file.write(yandex_info['text']['result']['alternatives'][0]['text'])