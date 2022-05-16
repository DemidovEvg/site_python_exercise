"""
Django settings for demidovsite project.

Generated by 'django-admin startproject' using Django 4.0.3.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import os
import mimetypes
from decouple import config
from pathlib import Path
from environs import Env
import sys

env = Env()
env.read_env()


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

os.environ['PYTHONPATH'] = str(BASE_DIR)
sys.path += str(BASE_DIR)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = config('DEBUG', default=False, cast=bool)
TEMPLATE_DEBUG = config('TEMPLATE_DEBUG', default=False, cast=bool)


mimetypes.add_type("application/javascript", ".js", True)

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

INTERNAL_IPS = [
    "127.0.0.1",
]


# Application definition

INSTALLED_APPS = [
    'channels',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'python_exercise.apps.PythonExerciseConfig',
    'custom_auth.apps.CustomAuthConfig',
    'debug_toolbar',
    'rest_framework',
    'snippets.apps.SnippetsConfig',
    'rest_framework.authtoken',
    'django_filters',
    'crispy_forms',
    'chat'
]

MIDDLEWARE = [
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'python_exercise.middleware.TimezoneMiddleware',

]

ROOT_URLCONF = 'demidovsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR/'templates'],
        'APP_DIRS': True,  # Ищем внутри установленных приложений
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'demidovsite.wsgi.application'
ASGI_APPLICATION = 'demidovsite.asgi.application'
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [('127.0.0.1', 6379), ],
        },
    }
}

# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'TEST': {
            'NAME': BASE_DIR / 'db_test.sqlite3'
        }
    }
}

print('parent id:', os.getppid(), ' :: ', 'process id:', os.getpid())

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


AUTH_USER_MODEL = 'custom_auth.CustomUser'

# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

USE_L10N = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

# STATIC_URL = 'static/'
# STATIC_ROOT = '/home/c/cl43553/jureti/public_html/static/'
# STATICFILES_DIRS = []

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR.parent / 'static'  # где файлы буду собираться
STATICFILES_DIRS = []

MEDIA_ROOT = BASE_DIR / 'media'
MEDIA_URL = '/media/'

# Для работы django-debug-toolbar. Позволяет включать/отключать
DEBUG_TOOLBAR_CONFIG = {
    'SHOW_TOOLBAR_CALLBACK': lambda r: False  # disables it
}


APP_ID_VK = config('APP_ID_VK')
SECRET_KEY_VK = config('SECRET_KEY_VK')

if DEBUG:

    LOGGING = {
        'version': 1,

        'disable_existing_loggers': False,

        'formatters': {
            'verbose': {
                'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
                'style': '{',
            },
            'simple': {
                'format': '{levelname} {asctime} {message}',
                'style': '{',
            },
        },

        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'rich.logging.RichHandler',
                'formatter': 'verbose'
            },
            'file': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': BASE_DIR/'logs/debug.log',
                'formatter': 'simple'
            },
        },

        'loggers': {

            'django': {
                'handlers': ['console'],
                'level': 'INFO',
                'filters': []
            },
            'demidovsite': {
                'handlers': ['file'],
                'level': 'INFO',
                'filters': [],
                'propagate': False,
            }
        }
    }

# Почта
# Для отладки сброса пароля пользователя
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = "smtp.timeweb.ru"

EMAIL_PORT = 2525

EMAIL_HOST_USER = "service@jureti.ru"

EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD')

SERVER_EMAIL = "service@jureti.ru"
DEFAULT_FROM_EMAIL = "service@jureti.ru"


# The cache backends to use.
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.filebased.FileBasedCache",
        "LOCATION": BASE_DIR/'tmp'
    }
}

# ========================================================
# Настройки REST
# ========================================================
REST_FRAMEWORK = {
    # 'DEFAULT_PERMISSION_CLASSES': [
    #     'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    # ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication'
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 3
}


CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
