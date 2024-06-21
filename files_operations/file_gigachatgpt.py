async def write_output_in_gigachat_file(gigachat_info):
    # Запись ответа на запрос от нейросети GIGACHAT в файл gigachat.txt
    with open("gigachat.txt", 'w', encoding='utf-8') as file:
        file.write(gigachat_info['text']["choices"][0]["message"]["content"])