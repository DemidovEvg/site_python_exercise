from django.db import models

from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField()

    class Meta:
        ordering = ('id',)


class UserData(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, null=False, verbose_name='Пользователь')
    photo_url = models.CharField(
        verbose_name='Фотография', max_length=255, blank=True, null=True)

    def __str__(self):
        return 'Данные для ' + str(self.user)

    def get_absolute_url(self):
        return self.photo_url

    class Meta:
        verbose_name = 'Данные пользователя'
        verbose_name_plural = 'Данные пользователя'
        ordering = ('id',)
