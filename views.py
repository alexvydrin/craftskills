"""Контроллеры"""
from storm import render


def main_view(request):
    """Контроллер главной страницы сайта"""
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    """Контроллер страницы About"""
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('about.html', secret=secret)
