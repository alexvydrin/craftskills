"""логгер"""
import time
from reusepatterns.singletones import SingletonByName


# Заметка, можно применить стратегию если добавить стратегию логирования
class Logger(metaclass=SingletonByName):  # pylint: disable=too-few-public-methods
    """логгер"""

    def __init__(self, name):
        self.name = name

    @staticmethod
    def log(text):
        """вносим запись о событии"""
        print('log--->', text)


def debug(func):
    """декоратор"""
    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG-------->', func.__name__, end - start)
        return result

    return inner
