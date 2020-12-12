"""Контроллеры"""
from storm import render


def main_view(request):
    """Контроллер главной страницы сайта"""
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('index.html', secret=secret)


def about_view(request):
    """Контроллер страницы 'О нас'"""
    secret = request.get('secret_key', None)
    # Используем шаблонизатор
    return '200 OK', render('about.html', secret=secret)


def contact_view(request):
    """Контроллер страницы Контакты"""
    # Проверяем метод запроса
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        text = data['text']
        email = data['email']
        message = f'Нам пришло сообщение от {email} с темой {title} и текстом {text}'
        print(message)
    else:
        message = ""

    # В любом случае выводим страницу контактов
    return '200 OK', render('contact.html', message=message)
