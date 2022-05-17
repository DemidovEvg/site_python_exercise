import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE',
                      'demidovsite.settings')

app = Celery('demidovsite')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()

# celery -A demidovsite worker --loglevel=INFO --concurrency 1 -P solo


@app.task(bind=True)
def debug_task(self):
    return 101

# result = debug_task.delay()
# result.ready()

# Превращает асинхронный вызов в синхронный:
# result.get(timeout=1)

# Без вызова исключения:
# result.get(propagate=False)

# Исходная трасировка в случае исключения:
# result.traceback
