"""Модели"""
import jsonpickle
from reusepatterns.prototypes import PrototypeMixin
from reusepatterns.observer import Subject, Observer
from storm_orm import DomainObject


class User:  # pylint: disable=too-few-public-methods
    """
    пользователи системы
    это могут быть преподаватели, студенты
    """

    def __init__(self, name):
        self.name = name


class Teacher(User):  # pylint: disable=too-few-public-methods
    """преподаватели"""
    # pass


class Student(User, DomainObject):  # pylint: disable=too-few-public-methods
    """студенты"""

    def __init__(self, name):
        self.courses = []
        super().__init__(name)


class UserFactory:  # pylint: disable=too-few-public-methods
    """фабрика для user"""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name):
        """создание user типа types[type_] -> Student, Teacher"""
        return cls.types[type_](name)


class Category:  # pylint: disable=too-few-public-methods
    """Категории курсов"""
    auto_id = 0

    def __init__(self, name, category):
        """инициализация категории"""
        self.id = Category.auto_id  # pylint: disable=invalid-name

        # print('Category.id=', self.id, name)

        Category.auto_id += 1  # автонумерация
        self.name = name
        self.category = category  # если эта категория вложена в другую категорию
        self.courses = []  # список курсов этой категории

    def __getitem__(self, item):
        """получить конкретный курс по номеру"""
        return self.courses[item]

    def course_count(self):
        """считаем сколько курсов содержит категория"""
        result = len(self.courses)

        # тут логика расчета неверная - потом можно переписать правильно
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin, Subject):
    """
    курс
    реализован паттерн прототип - для копирования курса
    """

    def __init__(self, name, category):
        self.name = name
        self.category = category  # какой категории принадлежит курс

        # print("category=", category)

        # print("=",category.name)

        self.category.courses.append(self)
        self.students = []  # список студентов на курсе
        super().__init__()

    def __getitem__(self, item):
        """получить конкретного студента по номеру"""
        return self.students[item]

    def add_student(self, student: Student):
        """добавить студента на курс"""
        self.students.append(student)
        student.courses.append(self)  # а студенту добавим этот курс
        self.notify()  # уведомляем всех студентов об изменении


class SmsNotifier(Observer):  # pylint: disable=too-few-public-methods
    """Уведомления по СМС"""

    # @staticmethod
    def update(self, subject):
        """
        сообщаем про присоединение нового студента
        subject: Course
        """
        print('SMS->', 'к нам присоединился', subject.students[-1].name)


class EmailNotifier(Observer):  # pylint: disable=too-few-public-methods
    """Уведомления по электронной почте"""

    # @staticmethod
    def update(self, subject):
        """
        сообщаем про присоединение нового студента
        subject: Course
        """
        print(('EMAIL->', 'к нам присоединился', subject.students[-1].name))


class BaseSerializer:
    """базовый класс для сериализации данных"""

    def __init__(self, obj):
        self.obj = obj  # объект для сериализации

    def save(self):
        """сохранение данных объекта в дамп"""
        return jsonpickle.dumps(self.obj)

    @staticmethod
    def load(data):
        """загрузка данных объекта из дампа"""
        return jsonpickle.loads(data)


class InteractiveCourse(Course):  # pylint: disable=too-few-public-methods
    """Интерактивный курс"""
    # pass


class RecordCourse(Course):  # pylint: disable=too-few-public-methods
    """Видеокурс"""
    # pass


class CourseFactory:  # pylint: disable=too-few-public-methods
    """Фабрика курсов"""
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        """создание нового курса"""
        return cls.types[type_](name, category)


class TrainingSite:
    """Интерфейс сайта"""

    def __init__(self):
        self.teachers = []  # преподаватели
        self.students = []  # студенты
        self.courses = []  # курсы
        self.categories = []  # категории курсов

    @staticmethod
    def create_user(type_, name):
        """создание нового пользователя"""
        return UserFactory.create(type_, name)

    @staticmethod
    def create_category(name, category=None):
        """создание новой категории курсов"""
        return Category(name, category)

    def find_category_by_id(self, id_):
        """поиск категории по ее номеру (id)"""
        for item in self.categories:

            # print('item', item.id)
            # print('name', item.name)

            if item.id == id_:
                return item
        raise Exception(f'Нет категории с id = {id_}')

    #
    # def get_or_create_category(self, name):
    #     for item in self.categories:
    #         if item.name == name:
    #             return item
    #     return self.create_category(name)

    @staticmethod
    def create_course(type_, name, category):
        """Создание нового курса"""
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):  # -> Course
        """поиск курса по его имени"""
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name):  # -> Student
        """поиск студента по его наименованию"""
        for item in self.students:
            if item.name == name:
                return item
        return None
