"""логгер"""
import time
from reusepatterns.singletones import SingletonByName


class ConsoleWriter:  # pylint: disable=too-few-public-methods
    """класс для вывода данных в консоль"""

    @staticmethod
    def write(text):
        """выводим данные в консоль"""
        print(text)


class FileWriter:  # pylint: disable=too-few-public-methods
    """класс для вывода данных в файл"""

    def __init__(self, file_name):
        self.file_name = file_name

    def write(self, text):
        """выводим данные в файл"""
        with open(self.file_name, 'a', encoding='utf-8') as file:
            file.write(f'{text}\n')


class Logger(metaclass=SingletonByName):  # pylint: disable=too-few-public-methods
    """
    Логгер
    """

    def __init__(self, name, writer=ConsoleWriter()):
        self.name = name
        self.writer = writer

    def log(self, text):
        """вносим запись о событии"""
        text = f'log---> {text}'
        self.writer.write(text)


def debug(func):
    """
    декоратор для view,
    при использовании декоратора над/перед view:
    в терминал выводятся название функции и время ее выполнения
    """

    def inner(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print('DEBUG-------->', func.__name__, end - start)
        return result

    return inner
