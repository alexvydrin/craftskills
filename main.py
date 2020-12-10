"""
Основная программа
# Запуск:
# gunicorn main:application
"""

from storm import Application
import views


# Определяем словарь связок url: view
urlpatterns = {
    '/': views.main_view,
    '/about/': views.about_view,
    '/contact/': views.contact_view,
}


# функции для front controllers:
def secret_controller(request):
    """пример Front Controller"""
    request['secret_key'] = 'SECRET'


# список front controllers
front_controllers = [
    secret_controller
]

application = Application(urlpatterns, front_controllers)
