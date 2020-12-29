"""
Основная программа
# Запуск:
# gunicorn main:application
"""

from models import TrainingSite, EmailNotifier, SmsNotifier, BaseSerializer
from logging_mod import Logger, debug
from storm import Application, render  # , DebugApplication, MockApplication
from storm.storm_cbv import ListView, CreateView
from storm_orm import UnitOfWork
from mappers import MapperRegistry


site = TrainingSite()
logger = Logger('main')
email_notifier = EmailNotifier()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

##########################################################################
# Первоначальные данные - пока нет БД для отладки

# Студенты
for student in MapperRegistry.get_current_mapper('student').all():
    # print(student.name)
    site.students.append(site.create_user('student', student.name))

# Категории
for category in MapperRegistry.get_current_mapper('category').all():
    # print("category.name=", category.name)
    site.categories.append(site.create_category(category.name, None))
    pass

_category = site.find_category_by_id(1*2)

# category_1 = site.create_category("Patterns")
# site.categories.append(category_1)
# category_2 = site.create_category("Patterns 2")
# site.categories.append(category_2)
site.courses.append(site.create_course('record', "Adapter", _category))
site.courses.append(site.create_course('record', "Bridge", _category))
site.courses.append(site.create_course('record', "Composite", _category))
site.courses.append(site.create_course('record', "Decorator", _category))
site.courses.append(site.create_course('record', "Facade", _category))
site.courses.append(site.create_course('record', "Proxy", _category))
# # Тестируем вложенные курсы и подсчет количества курсов
# category_AAA = site.create_category("Category_AAA")
# site.categories.append(category_AAA)
# category_BBB = site.create_category("Category_BBB")
# site.categories.append(category_BBB)
# category_AAA_1 = site.create_category("Category_AAA_1", category_AAA)
# site.categories.append(category_AAA_1)
# category_AAA_2 = site.create_category("Category_AAA_2", category_AAA)
# site.categories.append(category_AAA_2)
# site.courses.append(
#     site.create_course(
#         'record',
#         "Course_AAA_1_1",
#         category_AAA_1))
# site.courses.append(
#     site.create_course(
#         'record',
#         "Course_AAA_1_2",
#         category_AAA_1))
# site.courses.append(
#     site.create_course(
#         'record',
#         "Course_AAA_2_1",
#         category_AAA_2))
# site.courses.append(site.create_course('record', "Course_AAA_1", category_AAA))
# site.courses.append(site.create_course('record', "Course_AAA_2", category_AAA))
# site.courses.append(site.create_course('record', "Course_AAA_3", category_AAA))


# Курсы
# _category = site.find_category_by_id(1)

#for course in MapperRegistry.get_current_mapper('course').all():
#    print("course.name=", course.name)
    # site.courses.append(site.create_course(course.name, _category))


##########################################################################

# Контроллеры


def main_view(request):
    """Контроллер главной страницы сайта"""
    secret = request.get('secret_key', None)
    logger.log('Главная страница')
    # Используем шаблонизатор
    return '200 OK', render('index.html',
                            secret=secret, objects_list=site.courses)
    # return '200 OK', render('course_list.html',
    #                            objects_list=site.courses, secret=secret)


@debug
def create_course(request):
    """Контроллер - создание нового курса"""
    categories = site.categories
    if request['method'] == 'POST':
        # метод POST
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        # print(category_id)
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        course = site.create_course('record', name, category)
        # Добавляем наблюдателей на курс
        course.observers.append(email_notifier)
        course.observers.append(sms_notifier)
        site.courses.append(course)
    return '200 OK', render('create_course.html', categories=categories)


class CategoryCreateView(CreateView):
    """Контроллер - создание новой категории"""
    template_name = 'create_category.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['categories'] = site.categories
        return context

    def create_obj(self, data: dict):
        name = data['name']
        category_id = data.get('category_id')

        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))

        new_category = site.create_category(name, category)
        site.categories.append(new_category)


# def create_category(request):
#     """Контроллер - создание новой категории"""
#     if request['method'] == 'POST':
#         data = request['data']
#         # print(data)
#         name = data['name']
#
#         category = None
#         category_id = data.get('category_id')
#         if category_id:
#             category = site.find_category_by_id(int(category_id))
#
#         new_category = site.create_category(name, category)
#         site.categories.append(new_category)
#         return '200 OK', render('create_category.html')
#     # else:
#     categories = site.categories
#     return '200 OK', render('create_category.html', categories=categories)


def about_view(request):
    """Контроллер страницы 'О нас'"""
    secret = request.get('secret', None)
    # Используем шаблонизатор
    return '200 OK', render('about.html', secret=secret)


def contact_view(request):
    """
    Контроллер
    страница Контакты
    """
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


class CategoryListView(ListView):
    """Список категорий"""
    queryset = site.categories
    template_name = 'category_list.html'


class StudentListView(ListView):
    """Список студентов"""
    queryset = site.students
    template_name = 'student_list.html'

    # def get_queryset(self):
    #    mapper = MapperRegistry.get_current_mapper('student')
    #    return mapper.all()


class StudentCreateView(CreateView):
    """Создание нововго студента"""
    template_name = 'create_student.html'

    def create_obj(self, data: dict):
        name = data['name']
        new_obj = site.create_user('student', name)
        site.students.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()

class AddStudentByCourseCreateView(CreateView):
    """Добавление студента на курс"""
    template_name = 'add_student.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['courses'] = site.courses
        context['students'] = site.students
        return context

    def create_obj(self, data: dict):
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)

        print("course: ", course.name)
        print("student: ", student.name)

        course.add_student(student)

##########################################################################

# Определяем словарь связок url: view
urlpatterns = {
    '/': main_view,
    '/about/': about_view,
    '/contact/': contact_view,
    '/create-course/': create_course,
    '/create-category/': CategoryCreateView(),
    '/category-list/': CategoryListView(),
    '/student-list/': StudentListView(),
    '/create-student/': StudentCreateView(),
    '/add-student/': AddStudentByCourseCreateView(),
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


# Паттерн Proxy
# application = DebugApplication(urlpatterns, front_controllers)

# Паттерн Заместитель ?
# application = MockApplication(urlpatterns, front_controllers)

@application.add_route('/copy-course/')
def copy_course(request):
    """
    Копирование курса
    реализация паттерна Prototype
    """
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


# @application.add_route('/category-list/')
# def category_list(request):
#     """Список категорий курсов"""
#     logger.log('Список категорий')
#     secret = request.get('secret_key', None)
#     return '200 OK', render('category_list.html',
#                             objects_list=site.categories, secret=secret)


@application.add_route('/course-list/')
def course_list(request):
    """выводим список курсов"""
    secret = request.get('secret_key', None)
    logger.log('Список курсов')
    # Используем шаблонизатор
    return '200 OK', render('course_list.html',
                            objects_list=site.courses, secret=secret)


@application.add_route('/api/')
def course_api():  # request
    """API"""
    return '200 OK', BaseSerializer(site.courses).save()
