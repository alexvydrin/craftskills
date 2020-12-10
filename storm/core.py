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

    @staticmethod
    def parse_input_data(data: str):
        """
        парсим данные get-запроса
        :param data: данные get-запроса в виде строки с разделителями '&' и '='
        example: /some_url/?name=max&age=18 -> name=max&age=18
        :return: данные get-запроса в виде словаря
        """
        result = {}
        if data:
            # делим параметры через &
            params = data.split('&')

            for item in params:
                # делим ключ и значение через =
                key, value = item.split('=')
                result[key] = value

        # возвращаем словарь с полученными параметрами get-запроса
        return result

    def parse_wsgi_input_data(self, data: bytes):
        """
        парсим данные в виде набора байтов
        """
        result = {}
        if data:
            # декодируем данные
            data_str = data.decode(encoding='utf-8')
            # собираем их в словарь
            result = self.parse_input_data(data_str)
        return result

    @staticmethod
    def get_wsgi_input_data(env):
        """
        извлекаем данные post-запроса в виде набора байтов
        """
        # получаем длину тела
        content_length_data = env.get('CONTENT_LENGTH')
        # приводим к int
        content_length = int(content_length_data) if content_length_data else 0

        # считываем данные, если они есть
        data = b''
        if content_length > 0:
            data = env['wsgi.input'].read(content_length)

        return data

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

        # получаем все данные запроса
        method = env['REQUEST_METHOD']  # метод которым отправили запрос

        # получаем данные post-запроса в виде набора байтов
        data = self.get_wsgi_input_data(env)
        # превращаем данные post-запроса в словарь
        data = self.parse_wsgi_input_data(data)

        # получаем данные get-запроса
        query_string = env['QUERY_STRING']
        # превращаем данные get-запроса в словарь
        request_params = self.parse_input_data(query_string)

        if path in self.urlpatterns:
            # получаем view по url
            view = self.urlpatterns[path]

            # параметры запросов
            request = {
                'method': method,
                'data': data,
                'request_params': request_params}

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
