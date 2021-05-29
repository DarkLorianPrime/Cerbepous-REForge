"""
Это основной файл
Darklorian
@animanshnik (tg)
"""

import os

import dotenv

from projects.MediaSoft.diplom_tg import request_updater, command_registrator, Models

# Подключение модулей
link = f'{os.getcwd()}\config.env'
dotenv.load_dotenv(link)
request_updater.activate_bot(os.getenv('token'))
command_registrator.reg()
Models.connect_to_db()


# По идее необязательная часть, но для удобства, и в дань уважения python273 сделал.
for i in request_updater.updater():
    if i.get('message') is not None:
        text = i['message']['text']
        chat_id = i['message']['chat']['id']
        print(f'{chat_id}: {text}')
