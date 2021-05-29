"""
Darklorian
@animanshnik (tg)
"""

from projects.MediaSoft.diplom_tg import connection_to_mysql
import peewee

# Модель пользователя.
class User(connection_to_mysql.Base):
    user_id = peewee.CharField()
    last_message_id = peewee.CharField()
    chat_id = peewee.CharField()

    class Meta:
        db_table = 'User'
        order_by = 'id'


def connect_to_db():
    if not User.table_exists():
        User.create_table()
