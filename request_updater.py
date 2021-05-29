"""
Darklorian
@animanshnik (tg)
"""

import re

import requests
import peewee

from projects.MediaSoft.diplom_tg import Models

methods = 'https://api.telegram.org'
dict_for_methods, active_token, dict_for_methods_callback = {}, [], {}

# Основной файл подключения. Welcome to the club, buddy.


# Лично эта функция подключает КЛАВИАТУРНЫЕ функции. Тоже удобненько. Декоратор too
def handler_cb(*args_dict):
    def decorator(fn):
        dict_for_methods_callback[args_dict] = fn

        def wrapper(*args, **kwargs):
            return fn(args, kwargs)

        return wrapper

    return decorator


# Эта функция позволяет подключить через словарь все функции что есть. Сделано декоратором
def handler(*args_dict):
    def decorator(fn):
        dict_for_methods[args_dict] = fn

        def wrapper(*args, **kwargs):
            # Щас бы функцию не выполнять, лол.
            return fn(args, kwargs)

        return wrapper

    return decorator


# Один раз ввел токен - он у тебя на ВСЁ работает. Тоже удобно.
def activate_bot(token):
    active_token.append(token)
    return 'OK'


# Зачем использовать библиотеки os, path и тд? У нас свое есть!
def url_compiler(method):
    return f'{methods}/bot{active_token[0]}/{method}'


# Если какой-то приколист решит пропустить ввод токена. А мы хоба, и прикололись над ним. Хе-хе.
def token_checker():
    if len(active_token) != 1:
        raise Exception('Missing token\nAt the beginning of the file, specify the activate_bot (token) to get started')
    else:
        return True


# Оо.. Это достижение современных Лорианов. Позволяет выполнять ЛЮБЫЕ методы телеги без requestов. Ну, почти любые. Если они с POST, то ты отдыхаешь.
# Работает без нареканий, пробег пол дня. Не крашена, не бита.
class tg(object):
    def __init__(self, method=None):
        self.method = method

    def __getattr__(self, method):
        return tg(method)

    def __call__(self, *args, **kwargs):
        if self.method is None:
            raise Exception('Method not passed')
        url = url_compiler(self.method)
        r = requests.get(url, params=kwargs).json()
        # Если нужен вывод в консоль. Для дебага часто юзал: print(r)
        return r


# Самая костыльная функция этого проекта. Желательно вниз не смотреть. Ну, одним глазком можно.
# Если так подумать, мне кажется тут пол функции выкинуть можно, и она будет работать
# Но мой первый закон - Работает? Ну и не трогай. Главное чтоб без крашей.
def updater():
    r = None
    if token_checker():
        url = url_compiler('getUpdates')
        while True:
            response = requests.get(url, params={'offset': r})
            if response.json()['result']:
                if r == response.json()['result'][-1]['update_id']:
                    continue
                else:
                    r = response.json()['result'][-1]['update_id']
                    response = response.json()['result'][-1]
                    try:
                        if dict(response).get('message') is not None:
                            thg = Models.User.get(Models.User.user_id == dict(response).get('message')['from']['id'])
                            new_message_id = thg.last_message_id
                            thg.last_message_id = response['update_id']
                            thg.save()
                            if int(new_message_id) == int(response['update_id']):
                                tg().sendMessage(chat_id=response['message']['from']['id'],
                                                 text=f'Приветик! Мы немного уснули. Извини за неудобства! \n'
                                                      f'Если твоя последняя команда не была выполнена! То вот она: {response["message"]["text"]}\n '
                                                      f'Просто повтори ее! Если я еще раз усну, то напиши ему @animanshnik !')
                                continue
                            else:
                                yield response
                    except peewee.DoesNotExist:
                        Models.User(user_id=response['message']['from']['id'],
                                    chat_id=response['message']['chat']['id'],
                                    last_message_id=response['update_id']).save()
                    if response.get('message') is not None:
                        for j in dict_for_methods:
                            for z in j:
                                if re.search(z, response['message']['text']):
                                    dict_for_methods[j](response)
                    elif response.get('callback_query') is not None:
                        for g in dict_for_methods_callback:
                            for i in g:
                                if re.search(i, response['callback_query']['data']):
                                    dict_for_methods_callback[g](response)
            else:
                continue
