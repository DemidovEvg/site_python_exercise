from django.apps import AppConfig
from django.core.checks import register
from .checks import *


class PythonExerciseConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'python_exercise'

    def ready(self):
        from . import signals
        register()(example_check)
