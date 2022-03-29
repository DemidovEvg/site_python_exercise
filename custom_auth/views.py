import hashlib
import html
import logging
from pprint import pprint
from urllib.parse import unquote

from demidovsite.settings import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordResetCompleteView,
                                       PasswordResetConfirmView,
                                       PasswordResetDoneView,
                                       PasswordResetView)
from django.http import Http404, HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView

from .forms import *
from .models import *


class RegistrationUserView(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration.html'
    success_url = reverse_lazy('custom_auth:login')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация'
        return context


class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = 'login.html'
    slug_url_kwarg = 'error'

    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Вход'
        if context['form'].errors:
            context['form_errors'] = context['form'].errors['__all__']

        try:
            context['login_vk_error'] = self.kwargs['error']
        except:
            pass

        return context

    def get_success_url(self):
        url = self.request.POST.get('next')
        if not url:
            url = reverse_lazy('python_exercise:home')

        return url


class CustomLogoutView(LogoutView):
    template_name = 'logged_out.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Выход'
        return context


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('custom_auth:password_reset_done')
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'

    def __init__(self, *args, **kwargs):
        return PasswordResetView.__init__(self, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля'
        return context

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm
    success_url = reverse_lazy('custom_auth:password_reset_complete')
    template_name = 'password_reset_confirm.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля'
        return context


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля'
        return context


class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Сброс пароля'
        return context


def login_vk(request):
    if request.method != 'GET':
        # url = request.path
        # logging.warning(f'{url = } Method not GET')
        raise Http404('Method not GET')
    try:
        uid = request.GET['uid']
        user_hash_hex = request.GET['hash']
        first_name = request.GET['first_name']
        hash_calc = hashlib.md5(APP_ID_VK.encode('utf-8')
                                + uid.encode('utf-8')
                                + SECRET_KEY_VK.encode('utf-8'))
        if hash_calc.hexdigest() != user_hash_hex:
            raise Exception('Invalid hash')
    except Exception:
        return redirect(reverse('custom_auth:login_error',
                                kwargs={'error': 'no-data'}))

    # breakpoint()
    last_name = request.GET.get('last_name', '')
    photo_url = request.GET.get('photo', '')
    photo_url_small = request.GET.get('photo_rec', '')
    photo_url_small = html.unescape(unquote(photo_url_small))

    if not last_name or not photo_url or not photo_url_small:
        logger = logging.getLogger('demidovsite')
        logger.warning('One of the following is missing'
                       f'last_name = {last_name}, photo_url = {photo_url}, photo_url_small = {photo_url_small }')

    user = authenticate(username=uid, password=user_hash_hex)
    if user is None:
        # Создаем пользователя

        user = CustomUser.objects.create()
        user.username = uid
        user.set_password(user_hash_hex)
        user.first_name = first_name
        user.last_name = last_name
        userdata = UserData.objects.create(
            user=user, photo_url=photo_url_small)
        userdata.save()
        user.save()

    else:
        user.first_name = first_name
        user.last_name = last_name
        user.userdata.photo_url = photo_url_small
        user.userdata.save()
        user.save()

    login(request, user)
    return redirect(reverse('python_exercise:home'))
