from django.test import TestCase
from ..models import *
from django.urls import reverse
import hashlib
from demidovsite.settings import APP_ID_VK, SECRET_KEY_VK
from django.core import mail
import re


class TestAccessibleViewsTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Создадим 3 пользователя
        num_authors = 3
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

    def test_view_url_registration_accessible_by_name(self):
        response = self.client.get(reverse('custom_auth:registration'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_login_vk_accessible_by_name(self):
        # Делаем запрос GET без необходимых данных
        response = self.client.get(
            reverse('custom_auth:login_vk'), follow=True)

        self.assertRedirects(
            response,
            reverse('custom_auth:login_error',
                    kwargs={'error': 'no-data'}))

        # Считай плюс тест test_view_url_login_error_accessible_by_name
        self.assertContains(
            response,
            'Ошибка авторизации через VK',
            html=True)

        # Делаем запрос GET с данными пользователя
        uid = '8460766'
        user_hash = hashlib.md5(APP_ID_VK.encode('utf-8')
                                + uid.encode('utf-8')
                                + SECRET_KEY_VK.encode('utf-8'))

        user_hash_hex = user_hash.hexdigest()
        first_name = 'Ivan'
        last_name = 'Ivanovich'
        photo_url = 'no'
        photo_url_small = 'no'

        data = {
            'uid': uid,
            'first_name': first_name,
            'last_name': last_name,
            'hash': user_hash_hex
        }

        response = self.client.get(reverse('custom_auth:login_vk'), data=data)
        self.assertRedirects(
            response,
            reverse('python_exercise:home'))

        # Делаем запрос POST без необходимых данных
        response = self.client.post(reverse('custom_auth:login_vk'))
        self.assertEqual(response.status_code, 404)

        # Делаем запрос POST с необходимыми данными
        response = self.client.post(reverse('custom_auth:login_vk'), data=data)
        self.assertEqual(response.status_code, 404)

    def test_view_url_login_accessible_by_name(self):
        response = self.client.get(
            reverse('custom_auth:login'))

        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'user0',
            'password': '0',
        }

        response = self.client.post(reverse('custom_auth:login'), data=data)
        self.assertRedirects(
            response,
            reverse('python_exercise:home'))

    def test_view_url_logout_accessible_by_name(self):
        response = self.client.get(
            reverse('custom_auth:login'))

        self.assertEqual(response.status_code, 200)

        data = {
            'username': 'user0',
            'password': '0',
        }

        response = self.client.post(reverse('custom_auth:login'), data=data)
        response = self.client.get(reverse('custom_auth:logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_url_password_reset_accessible_by_name(self):
        # Заходим на страницу с вводом почты
        response = self.client.get(
            reverse('custom_auth:password_reset'))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ['password_reset_form.html'])

        # Отправляем почту на сервер
        response = self.client.post(reverse('custom_auth:password_reset'),
                                    data={'email': 'ivan0@mail.ru'})

        self.assertEqual(response.status_code, 302)
        self.assertTrue('testserver' in mail.outbox[0].subject)

        RE_URL = re.compile('https?:\/\/testserver.*\/')

        url_password_reset_confirm = RE_URL.findall(mail.outbox[0].body)[0]

        # Переходим по ссылке в письме
        response = self.client.get(url_password_reset_confirm, follow=True)
        self.assertEqual(response.status_code, 200)

        password = CustomUser.objects.get(email='ivan0@mail.ru').password
        csrfmiddlewaretoken = str(response.context[0]['csrf_token'])

        # Отправляем новый пароль на сервер
        response = self.client.post(
            response.request['PATH_INFO'],
            data={'csrfmiddlewaretoken': csrfmiddlewaretoken,
                  'new_password1': 'pFDass12DD3321',
                  'new_password2': 'pFDass12DD3321'},
            follow=True)

        self.assertEqual(response.status_code, 200)
        username = CustomUser.objects.get(email='ivan0@mail.ru').username

        # Логинимся с новым паролем
        login = self.client.login(username=username, password='pFDass12DD3321')
        self.assertTrue(login)
