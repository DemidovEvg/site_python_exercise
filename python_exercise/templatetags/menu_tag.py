from copy import deepcopy
from django import template
from python_exercise.models import *
from ..urls import *
from copy import deepcopy

register = template.Library()

menu = {
    'home': {
        'title': 'Главная страница',
    },
    'create_exercise': {
        'title': 'Добавить задачу',
    },
    'user_exercises': {
        'title': 'Мои задачи',
    },
    'contact': {
        'title': 'Обратная связь',
    },
    'registration': {
        'title': 'Регистрация',
    },
    'login': {
        'title': 'Войти',
    },
    'logout': {
        'title': 'Выйти',
    },
}


@register.inclusion_tag('python_exercise/menu_tag.html', takes_context=True)
def menu_tag(context):
    context['menu'] = deepcopy(menu)
    request = context['request']
    context['next'] = request.path_info
    context['timezones'] = common_timezones
    context['now'] = timezone.now()

    return context
