"""Основной модуль фреймворка storm"""


class Application:  # pylint: disable=too-few-public-methods
    """Основной класс фреймворка storm"""

    def __init__(self, urlpatterns: dict, front_controllers: list):
        """
        :param urlpatterns: словарь связок url: view
        :param front_controllers: список front controllers
        """
        self.urlpatterns = urlpatterns
        self.front_controllers = front_controllers

    def __call__(self, env, start_response):
        """
        :param env: словарь с данными запроса
        :param start_response: функция для ответа серверу (код ответа и заголовки)
        """

        # получаем текущий url
        path = env['PATH_INFO']

        # обработка отсутствия слеша в конце адреса
        if not path.endswith('/'):
            # если слеш отсутствует, то добавляем его
            path += '/'

        if path in self.urlpatterns:
            # получаем view по url
            view = self.urlpatterns[path]
            request = {}
            # добавляем в запрос данные из front controllers
            for controller in self.front_controllers:
                # для каждого элемента списка запускаем соответствующую функцию
                controller(request)
            # вызываем view, который определили для path и получаем результат
            code, text = view(request)
            # передаем код ответа и заголовки
            start_response(code, [('Content-Type', 'text/html')])
            # возвращаем тело ответа в виде списка из набора bite
            return [text.encode('utf-8')]

        # Если url нет в urlpatterns - то страница не найдена
        start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
        return [b"Not Found"]
