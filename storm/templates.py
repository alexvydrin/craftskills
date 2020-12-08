"""Шаблонизатор фреймворка"""
import os
from jinja2 import Template


def render(template_name, folder='templates', **kwargs):
    """
    :param template_name: имя шаблона
    :param folder: папка в которой ищем шаблон
    :param kwargs: параметры для передачи в шаблон
    :return:
    """
    file_path = os.path.join(folder, template_name)
    # Открываем шаблон по имени
    with open(file_path, encoding='utf-8') as file:
        # Читаем
        template = Template(file.read())
    # рендерим шаблон с параметрами
    return template.render(**kwargs)
