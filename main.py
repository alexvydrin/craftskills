"""
Основная программа
# Запуск:
# gunicorn main:application
"""

from storm import Application, render, DebugApplication, MockApplication
# import views
from models import TrainingSite
from logging_mod import Logger, debug


site = TrainingSite()
logger = Logger('main')

# Первоначальные данные
category_1 = site.create_category("Порождающие паттерны")
site.categories.append(category_1)
site.courses.append(site.create_course('record', "Абстрактная фабрика", category_1))
site.courses.append(site.create_course('record', "Фабричный метод", category_1))
site.courses.append(site.create_course('record', "Строитель", category_1))
site.courses.append(site.create_course('record', "Одиночка", category_1))
site.courses.append(site.create_course('record', "Прототип", category_1))

########################################################################################
"""Контроллеры"""

def main_view(request):
    """Контроллер главной страницы сайта"""
    # secret = request.get('secret_key', None)
    logger.log('Список курсов')
    # Используем шаблонизатор
    # return '200 OK', render('index.html', secret=secret)
    return '200 OK', render('course_list.html', objects_list=site.courses)


def create_course(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        print(category_id)
        # category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

            course = site.create_course('record', name, category)
            site.courses.append(course)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def create_category(request):
    if request['method'] == 'POST':
        # метод пост
        data = request['data']
        # print(data)
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        # редирект?
        # return '302 Moved Temporarily', render('create_course.html')
        # Для начала можно без него
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


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

########################################################################################

# Определяем словарь связок url: view
urlpatterns = {
    '/': main_view,
    '/about/': about_view,
    '/contact/': contact_view,
    '/create-course/': create_course,
    '/create-category/': create_category,
}

# функции для front controllers:
def secret_controller(request):
    """пример Front Controller"""
    request['secret_key'] = 'SECRET'
    request['secret'] = 'secret'


# список front controllers
front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)

@application.add_route('/copy-course/')
def copy_course(request):
    request_params = request['request_params']
    # print(request_params)
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)

    return '200 OK', render('course_list.html', objects_list=site.courses)


@application.add_route('/category-list/')
def category_list(request):
    logger.log('Список категорий')
    return '200 OK', render('category_list.html', objects_list=site.categories)
