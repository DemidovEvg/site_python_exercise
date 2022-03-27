from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, UsernameField, PasswordResetForm
from .models import *
from .models import CustomUser as User


#  === Форма создания нового пользователя =====================
class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(label='Логин*:',
                               max_length=100,
                               required=True,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control',
                                          'placeholder': '',
                                          'type': 'text',
                                          'id': 'user_name'
                                          }
                               ))

    first_name = forms.CharField(label='Имя*:',
                                 max_length=100,
                                 required=True,
                                 widget=forms.TextInput(
                                     attrs={'class': 'form-control',
                                            'placeholder': '',
                                            'type': 'text',
                                            'id': 'first_name'
                                            }
                                 ))

    last_name = forms.CharField(label='Фамилия:',
                                max_length=100,
                                required=False,
                                widget=forms.TextInput(
                                    attrs={'class': 'form-control sss',
                                           'placeholder': '',
                                           'type': 'text',
                                           'id': 'last_name'
                                           }
                                ))

    email = forms.EmailField(label='Email*:',
                             max_length=254,
                             required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': '',
                                        'type': 'text',
                                        'id': 'email_address'
                                        }
                             ))

    password1 = forms.CharField(
        label="Пароль*:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'align': 'center',
            'placeholder': ''
        }),
    )

    password2 = forms.CharField(
        label="Подтверждение пароля*:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'align': 'center',
            'placeholder': ''
        }),
    )

    class Meta:

        model = User

        fields = ('username', 'first_name', 'last_name',
                  'email', 'password1', 'password2', )

#  ======================================================================
#  === Форма входа для пользователя ============================================


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label="Логин:",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'type': 'text',
            'align': 'center',
            'placeholder': ''
        }),
    )

    password = forms.CharField(
        label="Пароль:",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'type': 'password',
            'align': 'center',
            'placeholder': ''
        }),
    )

#  ======================================================================
#  === Форма ввода почты для сброса пароля ==============================


class CustomPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email указанный при регистрации:',
                             max_length=254,
                             required=True,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control',
                                        'placeholder': 'email address',
                                        'type': 'text',
                                        'id': 'email_address'
                                        }
                             ))
