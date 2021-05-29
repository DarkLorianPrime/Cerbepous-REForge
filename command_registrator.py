"""
Darklorian
@animanshnik (tg)
"""

import json
import random

from projects.MediaSoft.diplom_tg import request_updater, safe_random_citates, logger, textovic

tg = request_updater.tg()
st = {'text': 'q', 'callback_data': 'q'}

dicts = {'inline_keyboard': []}


# Если видишь этот комментарий - проскролль колесиком раз 10, не смотри сюда. Вторая по костыльности функция после updater'а
def add_button(*args):
    k_e = len(args) // 2
    if k_e == 4:
        d = dicts['inline_keyboard'] + [
            [{'text': args[0], 'callback_data': args[1]}, {'text': args[2], 'callback_data': args[3]},
             {'text': args[4], 'callback_data': args[5]}, {'text': args[6], 'callback_data': args[7]}]]
    elif k_e == 3:
        d = dicts['inline_keyboard'] + [
            [{'text': args[0], 'callback_data': args[1]}, {'text': args[2], 'callback_data': args[3]},
             {'text': args[4], 'callback_data': args[5]}]]
    elif k_e == 2:
        d = dicts['inline_keyboard'] + [
            [{'text': args[0], 'callback_data': args[1]}, {'text': args[2], 'callback_data': args[3]}]]
    elif k_e == 1:
        d = dicts['inline_keyboard'] + [[{'text': args[0], 'callback_data': args[1]}]]
    else:
        return 'MAX 8 ARGS: "text", "callback_data" * 4'
    dicts['inline_keyboard'] = d


# Получение данных из этой каши запросов. Хотите это увидеть?
# {'ok': True, 'result': {'message_id': 375, 'from': {'id': 1800683859, 'is_bot': True, 'first_name': 'Цербер', 'username': 'cerbepous_bot'}, 'chat': {'id': 1353242961, 'first_name': 'Александр', 'last_name': 'Касимов', 'username': 'animanshnik', 'type': 'private'}, 'date': 1622300209, 'photo': [{'file_id': 'AgACAgQAAxkDAAIBd2CyVjF19TD8nqs_mHTskso0K8P4AAI7rDEbbyeNUUKugzvXbSa0sQHNMF0AAwEAAwIAA3MAAwFQAAIfBA', 'file_unique_id': 'AQADsQHNMF0AAwFQAAI', 'file_size': 1907, 'width': 82, 'height': 90}, {'file_id': 'AgACAgQAAxkDAAIBd2CyVjF19TD8nqs_mHTskso0K8P4AAI7rDEbbyeNUUKugzvXbSa0sQHNMF0AAwEAAwIAA20ABFAAAh8E', 'file_unique_id': 'AQADsQHNMF0ABFAAAg', 'file_size': 29923, 'width': 293, 'height': 320}, {'file_id': 'AgACAgQAAxkDAAIBd2CyVjF19TD8nqs_mHTskso0K8P4AAI7rDEbbyeNUUKugzvXbSa0sQHNMF0AAwEAAwIAA3gAAwNQAAIfBA', 'file_unique_id': 'AQADsQHNMF0AAwNQAAI', 'file_size': 119416, 'width': 733, 'height': 800}, {'file_id': 'AgACAgQAAxkDAAIBd2CyVjF19TD8nqs_mHTskso0K8P4AAI7rDEbbyeNUUKugzvXbSa0sQHNMF0AAwEAAwIAA3kAAwJQAAIfBA', 'file_unique_id': 'AQADsQHNMF0AAwJQAAI', 'file_size': 136273, 'width': 811, 'height': 885}]}}
def re_func(args):
    if dict(args[0]).get('callback_query'):
        chat_id = args[0]['callback_query']['message']['chat']['id']
        text = args[0]['callback_query']['message']['text']
        message_id = args[0]['callback_query']['message']['message_id']
        data = args[0]['callback_query']['data']
        return chat_id, text, message_id, data
    else:
        chat_id = args[0]['message']['chat']['id']
        text = args[0]['message']['text']
        message_id = args[0]['message']['message_id']
        return chat_id, text, message_id


# Функция, всем функциям функция кстати.
def reg():
    # Отправка имени и фамилии пользователя.
    @logger.logger('Function Who')
    @request_updater.handler('/тазашо', '/кто')
    def send_name(*args):
        chat_id, text, message = re_func(args)
        tg.sendMessage(chat_id=chat_id,
                       text=f"Я думаю, ты - {args[0]['message']['from']['first_name']} {args[0]['message']['from']['last_name']}, бяка!")
        tg.sendPhoto(chat_id=chat_id, photo='https://i.redd.it/nmib9xeajsb61.jpg')

    # Приветствие при первом заходе
    @logger.logger('Function Start')
    @request_updater.handler('/start')
    def hello(*args):
        chat_id, text, message = re_func(args)
        tg.sendMessage(chat_id=chat_id,
                       text=f'Привееетик! Меня зовут цербер, но ты можешь называть меня церберушей :З\nПожалуйста, общайся вежливо. Я не смогу тебе ничего сделать, но неприлично же?')
        tg.sendAnimation(chat_id=chat_id,
                         animation='http://img0.joyreactor.cc/pics/post/Игры-Cerberus-%28Helltaker%29-Helltaker-Helltaker-gif-5958898.gif')
        tg.sendMessage(chat_id=chat_id,
                       text='У меня кстати появилась офигенная Inline клавиатура\n***Если этот Лор конечно успел ее реализовать***\nНапиши /help чтобы узнать как ей пользоваться!')

    # /help. Кноооооооопачки))
    @logger.logger('Function Help')
    @request_updater.handler('/help')
    def Help(*args):
        r = json.dumps({'inline_keyboard': [[{"text": 'Open menu', 'callback_data': '/hlp1'}]]})
        tg.sendMessage(chat_id=args[0]['message']['chat']['id'], reply_markup=r, text='Help menu:')

    # Смотрю на эту функцию, и какая-то огрессия, и зубы скрипят. Ненавижу кнопки телеграмма(
    @logger.logger('Function HelpMenu')
    @request_updater.handler_cb('/hlp1', 'cb_start', '/history', 'exit', 'cb_who', 'cb_about', 'cb_about_bot',
                                'cb_hist', 'cb_mediasoft', 'pass')
    def help_pages(*args):
        chat_id, text, message_id, data = re_func(args)
        dicts['inline_keyboard'] = []
        # Подключение кнопочек. Посмотрел оригинальный json, волосы дыбом встали. А так - все удобненько. 'text', 'callback_data'
        add_button('🔥кто', 'cb_who', '🔥start', 'cb_start', '🔥about', 'cb_about', '🔥about_bot', 'cb_about_bot')
        add_button('🔥history', 'cb_hist', '🔥Mediasoft', 'cb_mediasoft')
        add_button('exit', 'exit')
        add_button('Эти', 'pass', 'Две', 'pass', 'Строки', 'pass', 'Показывают', 'pass')
        add_button('как', 'pass', 'работают', 'pass', 'кнопки', 'pass')
        r = json.dumps(dicts)
        # Дальше тоже желательно не читать
        if data == '/hlp1':
            tg.editMessageText(chat_id=chat_id, message_id=message_id, reply_markup=r, text='Help menu:')
        if data == 'cb_who':
            tg.editMessageText(chat_id=chat_id, reply_markup=r, message_id=message_id,
                               text='Эта команда позволяет узнать имя и фамилию аккаунта')
        if data == 'cb_start':
            tg.editMessageText(chat_id=chat_id, message_id=message_id, text='Прочитать вступление еще раз',
                               reply_markup=r, )
        if data == 'exit':
            tg.editMessageText(chat_id=chat_id, message_id=message_id, text='Хопа, и клавиатура схлопнулась.')
        if data == 'cb_about':
            tg.editMessageText(chat_id=chat_id, message_id=message_id, text='Наш создатель: \nvk: vk.com/animanshnik '
                                                                            '\ntg: @animanshnik'
                                                                            '\ngithub: https://github.com/DarkLorianPrime',
                               reply_markup=r, )
        if data == 'cb_mediasoft':
            tg.sendMessage(chat_id=chat_id, text=textovic.mediasoft)
        if data == 'cb_hist':
            tg.editMessageText(chat_id=chat_id, message_id=message_id, text='После команды напиши свою историю!\n'
                                                                            'Мы тебя внимательно выслушаем :З',
                               reply_markup=r)
        if data == 'cb_about_bot':
            tg.editMessageText(chat_id=chat_id, message_id=message_id,
                               text='Мы - бот для телеграмма модели cerber-1.\nПри использовании наших команд вы рискуете:'
                                    '\n😈1. Потерять пальцы\n😈2. Потерять душу'
                                    '\n🙋🏻‍♀️3. Получить прокрастинацию и замкнутся в себе. Стать тихим, замкнутым, необщительным. '
                                    '\n4. Получить 🐕🐕🐕 хороших друзей, но это если очень сильно повезет.'
                                    '\n🔥В основном происходит 1, но иногда, с нашим создателем например, происходит и 3.🔥'
                                    '\nУдачного пользования)🖤', reply_markup=r, )
        if data == 'pass':
            tg.sendMessage(chat_id=chat_id, text='Nothing find! He-he. Don`t touch this button! Please. Really, dont`t')

    # Рассказываешь рандомную историю - получаешь реакцию на нее.
    @request_updater.handler('/история', '/history')
    @logger.logger('Function history')
    def history(*args):
        chat_id, text, message_id = re_func(args)
        text = args[0]['message']['text'][8:]
        if text != '':
            tg.sendMessage(chat_id=chat_id,
                           text=f'{text}\n\n{safe_random_citates.citates[random.randint(0, len(safe_random_citates.citates)) - 1]}')
            tg.sendPhoto(chat_id=chat_id,
                         photo=safe_random_citates.citates_photo[
                             random.randint(0, len(safe_random_citates.citates_photo)) - 1])
        else:
            tg.sendMessage(chat_id=chat_id,
                           text='Мы вообще то историю ждали! Бяка >_<\nВстал и молчит тут. Перевелись рассказчики на земле Rусской!')

    @request_updater.handler('/mediasoft', '/медиасофт', '/mediasoftinfo', '/andreyprivet')
    @logger.logger('Function info about mediasoft')
    def mediasoft_info(*args):
        chat_id, text, message_id = re_func(args)
        tg.sendMessage(chat_id=chat_id,
                       text=textovic.mediasoft)
