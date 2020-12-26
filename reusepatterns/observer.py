"""
Реализация поведенческого паттерна
паттерн Observer - Наблюдатель
"""


class Observer:  # pylint: disable=too-few-public-methods
    """
    Наблюдатель
    наблюдает за Subject
    """

    def update(self, subject):
        """изменяет состояние при изменениях у наблюдателя"""
        # pass


class Subject:  # pylint: disable=too-few-public-methods
    """
    Объект для наблюдения
    Имеет список подписавщихся на него наблюдателей
    """

    def __init__(self):
        self.observers = []

    def notify(self):
        """оповещает подписанных на этот объект наблюдателей"""
        for item in self.observers:
            item.update(self)
