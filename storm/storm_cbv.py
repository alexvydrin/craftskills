"""
Реализация возжности использования представлений, основанных на классах
CBV - Class-based views)
"""

from .templates import render


class TemplateView:
    """
    базовый класс для последующего наследования
    """
    template_name = 'template.html'  # имя шаблона по умолчанию

    def get_context_data(self):
        """получить контекст для рендеринга"""
        return {}

    def get_template(self):
        """получить шаблон для рендеринга"""
        return self.template_name

    def render_template_with_context(self):
        """
        рендеринг шаблона и контекста
        """
        template_name = self.get_template()  # получаем шаблон
        context = self.get_context_data()  # получаем контекст

        # рендерим используя полученный шаблон и контекст
        return '200 OK', render(template_name, **context)

    def __call__(self, request):
        return self.render_template_with_context()


class ListView(TemplateView):
    """Стандартный просмотр списка"""
    queryset = []  # список объектов заданной модели
    template_name = 'list.html'  # имя шаблона по умолчанию
    context_object_name = 'objects_list'  # имя списка объектов по умолчанию

    def get_queryset(self):
        """
        получить список объектов заданной модели
        """
        print(self.queryset)
        return self.queryset

    def get_context_object_name(self):
        """
        получить имя списка объектов
        """
        return self.context_object_name

    def get_context_data(self):
        """получить контекст для рендеринга"""
        queryset = self.get_queryset()  # получаем список объектов заданной модели
        context_object_name = self.get_context_object_name()  # получаем имя списка объектов
        # формируем контекст для рендеринга
        context = {context_object_name: queryset}
        return context


class CreateView(TemplateView):
    """Стандартный режим добавления нового объекта"""
    template_name = 'create.html'  # имя шаблона по умолчанию

    def get_request_data(self, request: dict) -> dict:
        """получить словарь data из request"""
        return request['data']

    def create_obj(self, data: dict):
        """создание нового объекта"""
        # pass

    def __call__(self, request: dict):
        if request['method'] == 'POST':
            # метод пост
            data = self.get_request_data(request)
            self.create_obj(data)
            # редирект?
            # return '302 Moved Temporarily', render('create_course.html')
            # Для начала можно без него
            return self.render_template_with_context()
        # else:
        return super().__call__(request)
