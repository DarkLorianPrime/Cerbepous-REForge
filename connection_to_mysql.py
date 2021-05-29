"""
Darklorian
@animanshnik (tg)
"""

import peewee
import dotenv
import os

# Подключение к Mysql. Может крашить, потому что mysql сервер лютое *
link = f'{os.getcwd()}/config.env'
dotenv.load_dotenv(link)
host, user, db, passw, port = os.getenv('host'), os.getenv('user'), os.getenv('db'), os.getenv('password'), os.getenv(
    'port')
conn = peewee.MySQLDatabase(host=host, user=user, database=db, password=passw)


class Base(peewee.Model):
    class Meta:
        database = conn
