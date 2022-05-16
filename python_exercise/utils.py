from django.urls import resolve
from .models import *
from django.db.models import *
import re
import logging
import pprint
from django.utils import timezone


# def get_elements_from_obj(obj):
#     result = ''
#     for key in dir(obj):
#         try:
#             result += f'{key}\n'
#             value = pprint.pformat(obj.__getattribute__(key))
#             if "<WSGIRequest: GET '/'>>" in value:
#                 result += str(obj.__getattribute__(key)())
#             else:
#                 result += value
#             result += f'\n===========================================================================\n'

#         except:
#             pass
#     return result

common_timezones = {
    'London': 'Europe/London',
    'Paris': 'Europe/Paris',
    'New York': 'America/New_York',
}


class DataMixin:
    paginate_by = 2

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['cur_url_name'] = resolve(self.request.path_info).url_name
        context['home_url_name'] = 'home'

        # logger = logging.getLogger('demidovsite')
        # logger.critical('123')

        return context


def clean_data_from_js(data):
    def glue_elements(first, second):
        result = ''
        for i in range(len(first)):
            result += first[i]
            if i < len(second):
                result += second[i]
        return result

    # Отделим код от текста
    RE_PRE_CODE = re.compile(r"<pre.+?</pre>", re.DOTALL)
    codes = RE_PRE_CODE.findall(data)
    texts = RE_PRE_CODE.split(data)

    # Обработаем кодовые блоки
    # Для этого вначале выдерним все что между тегами <code></code>
    RE_CODE_PARSER = re.compile(
        r"""(?P<outter_code_left>.+?<code.*?>)
        (?P<inner_code>.+?)
        (?P<outter_code_right></code>.+)""", re.DOTALL | re.X)

    codes_tmp = []
    result = ''
    for code in codes:
        code_parser = RE_CODE_PARSER.search(code)
        # Теперь экранируем все угловые кавычки внутри
        inner_code = code_parser['inner_code'].replace(
            '<', '&lt;').replace('>', '&gt;')
        result += code_parser['outter_code_left']
        result += inner_code
        result += code_parser['outter_code_right']
        codes_tmp.append(result)

    codes = codes_tmp
    # ==============================================

    # Обработаем текстовые блоки
    # Для этого экранируем любые угловые скобки внутри текста,
    # кроме тех которые задают реальные теги форматирования:
    # <p>, <h1>, <h2>, <h3>, <h4>, <h5>, <h6>, </br>

    def shield_tags(text):
        RE_NEED_TAG = re.compile(
            r'&lt;(?P<tag_name>((/?p)|(/?h\d)|(br\s?/)))&gt;')

        result = re.sub('<', '&lt;', text)
        result = re.sub('>', '&gt;', result)
        result = RE_NEED_TAG.sub(r'<\g<tag_name>>', result)
        return result

    texts_tmp = []
    for text in texts:
        texts_tmp.append(shield_tags(text))

    texts = texts_tmp

    return glue_elements(texts, codes)
