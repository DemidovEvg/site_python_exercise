from django.test import TestCase
from ..models import *
from ..urls import *
from custom_auth.models import CustomUser


from random import randint


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

        status_code_redirect_permanent = 301

        self.assertRedirects(
            response,
            reverse('python_exercise:home'),
            status_code=status_code_redirect_permanent)

        # Пробуем сделать POST запрос на создание тега без регистрации
        response = self.client.post(
            reverse('python_exercise:create-tag'),
            data={'name': 'newTag'})

        self.assertRedirects(
            response,
            reverse('custom_auth:login'),
            status_code=status_code_redirect_permanent)

        # Пробуем сделать GET запрос на создание тега с регистрацией
        login = self.client.login(username='user0', password='0')

        response = self.client.get(
            reverse('python_exercise:create-tag'))

        self.assertRedirects(
            response,
            reverse('python_exercise:home'),
            status_code=status_code_redirect_permanent
        )
        # Пробуем сделать POST запрос на создание тега с регистрацией
        response = self.client.post(
            reverse('python_exercise:create-tag'),
            data={'name': 'newTag'},
            content_type="application/json")

        self.assertEqual(response.status_code, 200)

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

        self.assertEqual(response.status_code, 200)

    def test_view_url_user_exercises_update_accessible_by_name(self):
        self.test_view_url_user_exercises_accessible_by_name(
            'python_exercise:user_exercises_create')

    def test_view_url_user_exercises_update_accessible_by_name(self):
        self.test_view_url_user_exercises_accessible_by_name(
            'python_exercise:user_exercises_update')
