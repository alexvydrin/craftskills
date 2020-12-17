"""
Шаблонизатор фреймворка
Работа с шаблонами, паттерн INTERFACE
Используем шаблонизатор jinja2
"""
# import os
# from jinja2 import Template
from jinja2 import FileSystemLoader
from jinja2.environment import Environment


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры для передачи в шаблон
    :return:
    """

    # Старый вариант
    # file_path = os.path.join(folder, template_name)
    # # Открываем шаблон по имени
    # with open(file_path, encoding='utf-8') as file:
    #     # Читаем
    #     template = Template(file.read())

    env = Environment()

    # указываем папку для поиска шаблонов
    env.loader = FileSystemLoader(folder)

    # находим шаблон в окружении
    template = env.get_template(template_name)

    # рендерим шаблон с параметрами
    return template.render(**kwargs)
