from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView
from .forms import *
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.contrib.auth import authenticate, login
from .models import *
import hashlib
from demidovsite.settings import *
from urllib.parse import unquote
import html


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

    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Вход'
        if context['form'].errors:
            context['form_errors'] = context['form'].errors['__all__']

        try:
            context['login_vk_status'] = self.kwargs['status']
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


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm
    success_url = reverse_lazy('password_reset_done')
    template_name = 'password_reset_form.html'
    email_template_name = 'password_reset_email.html'


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    success_url = reverse_lazy('password_reset_complete')
    template_name = 'password_reset_confirm.html'


class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'


def login_vk(request):

    try:
        uid = request.GET['uid']
        hash = request.GET['hash']
        first_name = request.GET['first_name']
        last_name = request.GET['last_name']
        photo_url = request.GET['photo']
        photo_url_small = request.GET['photo_rec']
        photo_url_small = html.unescape(unquote(photo_url_small))
        hash_calc = hashlib.md5(APP_ID_VK.encode('utf-8')
                                + uid.encode('utf-8')
                                + SECRET_KEY_VK.encode('utf-8'))
        if hash_calc.hexdigest() != hash:
            raise Exception('Invalid hash')
    except Exception:
        return redirect(reverse('custom_auth:login'), kwargs={'login_vk_status': 'fault'})

    user = authenticate(username=uid, password=hash)
    if user is None:
        # Создаем пользователя

        user = CustomUser.objects.create()
        user.username = uid
        user.set_password(hash)
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
