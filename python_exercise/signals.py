from django.core.signals import request_finished
from django.dispatch import receiver
from .views import *


@receiver(signal=request_finished)
def callback(sender, **kwargs):
    pass
    # print('< Вызвана функция python_exercise.signals.callback по сигналу request_finished. >')
