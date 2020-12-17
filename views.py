"""Контроллеры"""
from storm import render


def main_view(request):
    """Контроллер главной страницы сайта"""
    # secret = request.get('secret_key', None)
    # logger.log('Список курсов')
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
