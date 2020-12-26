"""
Реализация порождающего паттерна
паттерн Одиночка
"""


class SingletonByName(type):
    """Одиночка или синглтон"""

    def __init__(cls, name, bases, attrs):  # **kwargs
        super().__init__(name, bases, attrs)
        cls.__instance = {}

    def __call__(cls, *args, **kwargs):
        name = None
        if args:
            name = args[0]
        if kwargs:
            name = kwargs['name']

        if name in cls.__instance:
            return cls.__instance[name]
        # else:
        cls.__instance[name] = super().__call__(*args, **kwargs)
        return cls.__instance[name]
