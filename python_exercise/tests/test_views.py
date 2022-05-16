import urllib
from random import randint

from custom_auth.models import CustomUser
from django.test import TestCase

from ..models import *
from ..urls import *


class AccessibleViewsTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        # Создадим 5 заданий, 3 категории, 3 тега, 3 авторов
        number_of_exercises = 5
        num_categories = 3
        num_tags = 3
        num_authors = 3

        for num_categorie in range(num_categories):
            cat = Category.objects.create(
                id=num_categorie,
                name=f'Категория {num_categorie}',
                complexity=num_categorie,
                slug=f'cat{num_categorie}')

            cat.save()

        for num_tag in range(num_tags):
            tag = Tag.objects.create(
                id=num_tag,
                name=f'Тег {num_tag}',
                slug=f'tag{num_tag}')

            tag.save()

        for num_author in range(num_authors):
            newUser = CustomUser.objects.create(
                id=num_author,
                username=f'user{num_author}',
                first_name=f'Иван{num_author}',
                last_name=f'Петров{num_author}',
                email=f'ivan{num_author}@mail.ru',
            )
            newUser.set_password(str(num_author))
            newUser.save()

        for num_exercise in range(number_of_exercises):
            exercise = Exercise.objects.create(
                id=num_exercise,
                title=f'Задание{num_exercise}',
                task_text='''
                <p>Некоторый текст<p>
                <p onclick='dangerScript.js'> Запрещенный параграф </p>
                <script>
                alert(111);
                </script>
                <pre class="language-python"><code>
                import pprint
                <script>
                alert(1111);
                </script>
                </code></pre>
                ''',
                category=Category.objects.get(pk=randint(0, 2)),
                author_update=CustomUser.objects.get(pk=randint(0, 2)))

            exercise.tag.add(Tag.objects.get(pk=randint(0, 2)))

            exercise.save()

    def test_view_url_home_accessible_by_name(self):
        response = self.client.get(reverse('python_exercise:home'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_tag_accessible_by_name(self):
        response = self.client.get(
            reverse('python_exercise:tag',
                    kwargs={'tag_slug': Tag.objects.all()[0].slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_url_category_accessible_by_name(self):
        response = self.client.get(
            reverse('python_exercise:category',
                    kwargs={'category_slug': Category.objects.all()[0].slug}))
        self.assertEqual(response.status_code, 200)

    def test_view_url_category_and_tag_accessible_by_name(self):
        response = self.client.get(
            reverse('python_exercise:category_and_tag',
                    kwargs={'category_slug': Category.objects.all()[0].slug,
                            'tag_slug': Tag.objects.all()[0].slug
                            }))
        self.assertEqual(response.status_code, 200)

    def test_view_url_create_exercise_accessible_by_name(self):
        url = reverse('python_exercise:create-exercise')
        response = self.client.get(url)

        self.assertRedirects(
            response,
            reverse('custom_auth:login') +
            f"?next={url}")

    def test_view_url_create_tag_get_accessible_by_name(self):
        # Пробуем сделать GET запрос на создание тега без регистрации
        response = self.client.get(
            reverse('python_exercise:create-tag'))

        self.assertEqual(response.status_code, 405)

        # Пробуем сделать POST запрос на создание тега без регистрации
        response = self.client.post(
            reverse('python_exercise:create-tag'),
            data={'name': 'newTag'})

        status_code_redirect_permanent = 301

        self.assertRedirects(
            response,
            reverse('custom_auth:login'),
            status_code=status_code_redirect_permanent)

        # Пробуем сделать POST запрос на создание тега с регистрацией
        login = self.client.login(username='user0', password='0')
        self.assertTrue(login)
        response = self.client.post(
            reverse('python_exercise:create-tag'),
            data={'name': 'newTag'},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

        self.assertTrue(Tag.objects.filter(name='newTag').count())

    def test_view_url_update_exercise_accessible_by_name(self):
        # Пробуем редактировать задачу без регистрации
        any_exercise_id = 0
        url = reverse('python_exercise:update-exercise',
                      kwargs={'exercise_id': any_exercise_id})

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('custom_auth:login') +
            f"?next={url}"
        )

        # Пробуем редактировать задачу с регистрацией
        login = self.client.login(username='user0', password='0')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vies_url_exercise_accessible_by_name(self):
        any_exercise_id = 1
        response = self.client.get(reverse(
            'python_exercise:exercise',
            kwargs={'exercise_id': any_exercise_id}))

        self.assertEqual(response.status_code, 200)

        any_exercise_id = 222

        response = self.client.get(reverse(
            'python_exercise:exercise',
            kwargs={'exercise_id': any_exercise_id}))

        self.assertEqual(response.status_code, 404)

    def test_view_url_user_exercises_accessible_by_name(self, url_name=None):
        # Пробуем посмотреть задачи пользователя без регистрации
        any_username = CustomUser.objects.get(pk=0).username
        password = '0'
        if not url_name:
            url_name = 'python_exercise:user_exercises'

        url = reverse(
            f'{url_name}',
            kwargs={'username': any_username})

        response = self.client.get(url)
        self.assertRedirects(
            response,
            reverse('custom_auth:login') +
            f"?next={url}"
        )

        # Пробуем посмотреть задачи для зарегистрированного пользователя
        login = self.client.login(
            username=any_username,
            password=password)

        response = self.client.get(url)

        breakpoint()

        self.assertEqual(response.status_code, 200)

    def test_view_url_user_exercises_create_accessible_by_name(self):
        self.test_view_url_user_exercises_accessible_by_name(
            'python_exercise:user_exercises_create')

    def test_view_url_user_exercises_update_accessible_by_name(self):
        self.test_view_url_user_exercises_accessible_by_name(
            'python_exercise:user_exercises_update')


class CreateUpdateExerciseTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создадим 5 заданий, 3 категории, 3 тега, 3 авторов
        number_of_exercises = 5
        num_categories = 3
        num_tags = 3
        num_authors = 3

        for num_categorie in range(num_categories):
            cat = Category.objects.create(
                id=num_categorie,
                name=f'Категория {num_categorie}',
                complexity=num_categorie,
                slug=f'cat{num_categorie}')

            cat.save()

        for num_tag in range(num_tags):
            tag = Tag.objects.create(
                id=num_tag,
                name=f'Тег {num_tag}',
                slug=f'tag{num_tag}')

            tag.save()

        for num_author in range(num_authors):
            newUser = CustomUser.objects.create(
                id=num_author,
                username=f'user{num_author}',
                first_name=f'Иван{num_author}',
                last_name=f'Петров{num_author}',
                email=f'ivan{num_author}@mail.ru',
            )
            newUser.set_password(str(num_author))
            newUser.save()

        for num_exercise in range(number_of_exercises):
            exercise = Exercise.objects.create(
                id=num_exercise,
                title=f'Задание{num_exercise}',
                task_text='''
                <p>Некоторый текст<p>
                <p onclick='dangerScript.js'> Запрещенный параграф </p>
                <script>
                alert(111);
                </script>
                <pre class="language-python"><code>
                import pprint
                <script>
                alert(1111);
                </script>
                </code></pre>
                ''',
                category=Category.objects.get(pk=randint(0, 2)),
                author_update=CustomUser.objects.get(pk=randint(0, 2)))

            exercise.tag.add(Tag.objects.get(pk=randint(0, 2)))

            exercise.save()

    def test_create_new_exercise(self):
        # Пробуем создать задачу без авторизации
        data = {
            'title': f'Новое задание',
            'task_text': '''
                <p>Некоторый текст<p>
                <p onclick='dangerScript.js'> Запрещенный параграф </p>
                <script>
                alert(111);
                </script>
                <pre class="language-python"><code>
                import pprint
                <script>
                alert(1111);
                </script>
                </code></pre>
                ''',
            'is_published': True,
            'category': 1,
            'tag': (1,)
        }

        url = reverse('python_exercise:create-exercise')

        response = self.client.post(
            url,
            data=data)

        params = {'next': url}
        self.assertRedirects(response,
                             reverse('custom_auth:login')
                             + f'?{urllib.parse.urlencode(params)}',
                             status_code=302)

        self.assertFalse(Exercise.objects.filter(
            title='Новое задание').count())

        # Пробуем создать задачу c авторизацией
        login = self.client.login(username='user0', password='0')

        response = self.client.post(
            url,
            data=data)

        new_exercise = Exercise.objects.get(title='Новое задание')
        self.assertTrue(new_exercise)
        self.assertRedirects(response,
                             reverse('python_exercise:exercise',
                                     kwargs={'exercise_id': new_exercise.id}),
                             status_code=302)

    def test_update_new_exercise(self):
        # Пробуем редактировать задачу без авторизации
        any_exrcise = Exercise.objects.get(pk=1)
        data = {
            'title': any_exrcise.title,
            'task_text': any_exrcise.task_text + 'new_text',
            'is_published': any_exrcise.is_published,
            'category': any_exrcise.category_id,
            'tag': (any_exrcise.tag.all()[0].id,)
        }

        url = reverse('python_exercise:update-exercise',
                      kwargs={'exercise_id': any_exrcise.id})

        response = self.client.post(
            url,
            data=data)

        params = {'next': url}
        self.assertRedirects(response,
                             reverse('custom_auth:login')
                             + f'?{urllib.parse.urlencode(params)}',
                             status_code=302)

        any_exrcise_update = Exercise.objects.get(pk=1)

        self.assertFalse('new_text' in any_exrcise_update.task_text)

        # Пробуем изменить задачу c авторизацией
        login = self.client.login(username='user0', password='0')

        response = self.client.post(
            url,
            data=data)

        any_exrcise_update = Exercise.objects.get(pk=1)

        self.assertTrue('new_text' in any_exrcise_update.task_text)
        self.assertRedirects(response,
                             reverse('python_exercise:exercise',
                                     kwargs={'exercise_id': any_exrcise_update.id}),
                             status_code=302)


class ConditionTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создадим 5 заданий, 3 категории, 3 тега, 3 авторов
        number_of_exercises = 5
        num_categories = 3
        num_tags = 3
        num_authors = 3

        for num_categorie in range(num_categories):
            cat = Category.objects.create(
                id=num_categorie,
                name=f'Категория {num_categorie}',
                complexity=num_categorie,
                slug=f'cat{num_categorie}')

            cat.save()

        for num_tag in range(num_tags):
            tag = Tag.objects.create(
                id=num_tag,
                name=f'Тег {num_tag}',
                slug=f'tag{num_tag}')

            tag.save()

        for num_author in range(num_authors):
            newUser = CustomUser.objects.create(
                id=num_author,
                username=f'user{num_author}',
                first_name=f'Иван{num_author}',
                last_name=f'Петров{num_author}',
                email=f'ivan{num_author}@mail.ru',
            )
            newUser.set_password(str(num_author))
            newUser.save()

        for num_exercise in range(number_of_exercises):
            exercise = Exercise.objects.create(
                id=num_exercise,
                title=f'Задание{num_exercise}',
                task_text='''
                <p>Некоторый текст<p>
                <p onclick='dangerScript.js'> Запрещенный параграф </p>
                <script>
                alert(111);
                </script>
                <pre class="language-python"><code>
                import pprint
                <script>
                alert(1111);
                </script>
                </code></pre>
                ''',
                category=Category.objects.get(pk=randint(0, 2)),
                author_update=CustomUser.objects.get(pk=randint(0, 2)))

            exercise.tag.add(Tag.objects.get(pk=randint(0, 2)))

            exercise.save()

    def test_condition(self):
        # Проверяем метки в представлении
        headers = {'HTTP_IF_MATCH': '"v2"'}
        response = self.client.get(reverse('python_exercise:home'), **headers)
        self.assertEqual(response.status_code, 412)

        headers = {'HTTP_IF_NONE_MATCH': '"v1"'}
        response = self.client.get(reverse('python_exercise:home'), **headers)
        self.assertEqual(response.status_code, 304)
