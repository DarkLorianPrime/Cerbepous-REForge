"""
Darklorian
@animanshnik (tg)
"""

import os
import time


# Куда же без оптимизации. Если краш в логгерных функциях - то это не краш, а так, ошибочка.
def logger(info=None):
    rw = open(f'{os.getcwd()}/Logs.log', 'a+')
    if info is not None:
        rw.write(f'{"=" * 10}\n')
        rw.write(f'{time.strftime("/%H:%M:%S/")} [Function Loaded] name: {info} \n')

    def logger_dec(fn):
        def logger_wrap(*args):
            rw_log = open(f'{os.getcwd()}/Logs.log', 'a+')
            rw_log.write(f'{"=" * 10}\n')
            # Вот именно это не дает крашиться.
            try:
                returned = fn(*args)
                print(f'{fn.__name__} successful execute.')
                rw_log.write(f'{time.strftime("/%H:%M:%S/")} [LOADED] {fn.__name__} successful execute. \n')
            except Exception as ex:
                returned = args
                rw_log.write(
                    f'{time.strftime("/%H:%M:%S/")} [ERROR] Function [{fn.__name__}] Loading error: \n {ex} \n')
                print(
                    '[ERROR]Error, look at the information in the logs!\n[ERROR]Function returned the original value!')
            rw_log.close()
            return returned

        return logger_wrap

    return logger_dec
