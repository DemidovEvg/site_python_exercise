![Website](https://img.shields.io/website?url=http%3A%2F%2Fjureti.ru%2F)
![GitHub last commit](https://img.shields.io/github/last-commit/demidovevg/site_python_exercise)
[![made-with-django](https://img.shields.io/badge/Made%20with-Django-1f425f.svg)](https://docs.djangoproject.com/)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![made-with-javascript](https://img.shields.io/badge/Made%20with-JavaScript-1f425f.svg)](https://www.javascript.com)
<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="99" height="20">
    <linearGradient id="b" x2="0" y2="100%">
        <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
        <stop offset="1" stop-opacity=".1"/>
    </linearGradient>
    <mask id="a">
        <rect width="99" height="20" rx="3" fill="#fff"/>
    </mask>
    <g mask="url(#a)">
        <path fill="#555" d="M0 0h63v20H0z"/>
        <path fill="#4c1" d="M63 0h36v20H63z"/>
        <path fill="url(#b)" d="M0 0h99v20H0z"/>
    </g>
    <g fill="#fff" text-anchor="middle" font-family="DejaVu Sans,Verdana,Geneva,sans-serif" font-size="11">
        <text x="31.5" y="15" fill="#010101" fill-opacity=".3">coverage</text>
        <text x="31.5" y="14">coverage</text>
        <text x="80" y="15" fill="#010101" fill-opacity=".3">95%</text>
        <text x="80" y="14">95%</text>
    </g>
</svg>



# Учебный сайт с задачами по Python

Данный проект - сайт создан в учебных целях. Сайт содержит задачи для языка программирования python.

Frontend выполнен с использованием bootstrap 5 framework. 
Backend выполнен на Django framework.

Сайт представлен по [ссылке](http://jureti.ru/).
Если ссылка не доступна, то полноразмерные скриншоты:
- [спискок заданий](/screenshots/1.png), 
- [редактирование задачи](/screenshots/2.png), 
- [вход на сайт](/screenshots/3.png), 
- [карточка задачи с комментариями](/screenshots/4.png)

## Основной функционал:
- Фильтр задач по категориям и тегам.
- Создание новых задач. Функционал доступен для зарегистрированных пользователей.
- Редактирование существующих задач. Функционал доступен для зарегистрированных пользователей.
- Просмотр своих задач. Функционал доступен для зарегистрированных пользователей.
- Авторизация через логин, пароль, а также через widget VK.
- Комментирование задач.


## Особенности реализации
### Форма создания-редактирования задачи
Особенности:
- Поле textarea, вставляемое Django, автоматически подменяется на специальный редактор через сторонний плагин [TinyMCE](https://www.tiny.cloud/).
Данный редактор позволяет использовать продвинутые функции для форматирования текста. Для форматирования кода применяется сторонний плагин [prism](https://prismjs.com/).
Так как для последующей отрисовки требуется сохранить специальные теги форматирования (пример содержимого поля [task_text](/screenshots/6.png) в базе данных), в шаблоне Django данные вставлялись с фильтром safe(то есть без замены специальных символов). Так как существует угроза ввода в поле кода JavaScript, который при отрисовке выполнится на стороне клиента(угроза [XSS](https://en.wikipedia.org/wiki/Cross-site_scripting)), все угловые скобки, которые не относятся к основным тегам форматирования преобразовывались в специальный не исполняемый [html-код](https://dev.w3.org/html5/html-author/charref) ([пример кода задачи](/screenshots/7.png)). Алгоритм реализован на JavaScript.
- Для удобства нахождения тегов, одно поле multiple заменяется на отдельные поля для каждого тега. Для этого данные с каждого отдельного поля, после нажатия кнопки submit передавались в объект ([multiple](/screenshots/5.png)). При редактировании задачи данные наоборот передаются из multiple в одиночные поля тегов. Алгоритм реализован на [JavaScript](python_exercise/static/python_exercise/js/create-update-exercise.js).

### Регистрация и авторизация
Реализована как стандартная регистрация и авторизация так и через widget VK. Для этого использовался следующий [API](https://dev.vk.com/widgets/auth).

### Комментарии
Для осуществления функционала комментирования использовался widget VK. Данная реализация привязывает для каждой отдельной страницы свой набор комментариев, которые можно администрировать. 


Что проект делает?
Как им пользоваться?
