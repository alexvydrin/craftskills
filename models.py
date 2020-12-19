"""Модели"""
from reusepatterns.prototypes import PrototypeMixin


class User:  # pylint: disable=too-few-public-methods
    """
    пользователи системы
    это могут быть преподаватели, студенты
    """
    # pass


class Teacher(User):  # pylint: disable=too-few-public-methods
    """преподаватели"""
    # pass


class Student(User):  # pylint: disable=too-few-public-methods
    """студенты"""
    # pass


# не используется
# class SimpleFactory:  # pylint: disable=too-few-public-methods
#     """Фабричный метод"""
#     def __init__(self, types=None):
#         self.types = types or {}


class UserFactory:  # pylint: disable=too-few-public-methods
    """фабрика для user"""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        """создание user типа types[type_] -> Student, Teacher"""
        return cls.types[type_]()


class Category:  # pylint: disable=too-few-public-methods
    """Категории курсов"""
    auto_id = 0

    def __init__(self, name, category):
        """инициализация категории"""
        self.id = Category.auto_id  # pylint: disable=invalid-name
        Category.auto_id += 1  # автонумерация
        self.name = name
        self.category = category  # если эта категория вложена в другую категорию
        self.courses = []  # список курсов этой категории

    def course_count(self):
        """считаем сколько курсов содержит категория"""
        result = len(self.courses)

        # тут пока не могу понять логику расчета
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin):  # pylint: disable=too-few-public-methods
    """
    курс
    реализован паттерн прототип - для копирования курса
    """

    def __init__(self, name, category):
        self.name = name
        self.category = category  # какой категории принадлежит курс
        self.category.courses.append(self)


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
    def create_user(type_):
        """создание нового пользователя"""
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        """создание новой категории курсов"""
        return Category(name, category)

    def find_category_by_id(self, id_):
        """поиск категории по ее номеру (id)"""
        for item in self.categories:
            # print('item', item.id)
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
