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


class SimpleFactory:  # pylint: disable=too-few-public-methods
    """Фабричный метод"""
    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:  # pylint: disable=too-few-public-methods
    """фабрика для user"""
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_):
        """создание"""
        return cls.types[type_]()


class Category:  # pylint: disable=too-few-public-methods
    """реестр?"""
    auto_id = 0

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin):  # pylint: disable=too-few-public-methods

    def __init__(self, name, category):
        self.name = name
        self.category = category
        self.category.courses.append(self)


class InteractiveCourse(Course):  # pylint: disable=too-few-public-methods
    pass


class RecordCourse(Course):  # pylint: disable=too-few-public-methods
    pass


class CourseFactory:  # pylint: disable=too-few-public-methods
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name, category):
        return cls.types[type_](name, category)


class TrainingSite:
    # Интерфейс
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    @staticmethod
    def create_user(type_):
        return UserFactory.create(type_)

    @staticmethod
    def create_category(name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id_):
        for item in self.categories:
            print('item', item.id)
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
        return CourseFactory.create(type_, name, category)

    def get_course(self, name):  # -> Course
        for item in self.courses:
            if item.name == name:
                return item
        return None
