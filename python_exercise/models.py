from django.db import models
from django.urls import reverse
from demidovsite.settings import AUTH_USER_MODEL as User


class Exercise(models.Model):
    title = models.CharField(
        verbose_name='Название задачи',
        max_length=255)

    task_text = models.TextField(
        verbose_name='Текст задачи')

    is_published = models.BooleanField(
        verbose_name='Публикация',
        default=True)

    category = models.ForeignKey(
        verbose_name='Категория',
        to='Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True)

    tag = models.ManyToManyField(
        verbose_name='Тег',
        to='Tag',
        blank=True)

    time_create = models.DateTimeField(
        verbose_name='Дата и время создания',
        auto_now_add=True)

    author_create = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор создания',
        related_name='%(class)s_created')

    time_update = models.DateTimeField(
        verbose_name='Дата и время изменения',
        auto_now=True)

    author_update = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Автор последних изменений',
        related_name='%(class)s_update')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('python_exercise:exercise', kwargs={'exercise_id': self.id})

    def get_absolute_url_update(self):
        return reverse('python_exercise:update-exercise', kwargs={'exercise_id': self.id})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-time_update',)


class Category(models.Model):
    name = models.CharField(verbose_name='Категория', max_length=255)
    complexity = models.IntegerField(verbose_name='Сложность')
    # color = models.CharField(verbose_name='Сложность', max_length=255)
    slug = models.SlugField(verbose_name='URL', max_length=255)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('python_exercise:category', kwargs={'category_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ('id',)
        permissions = (("can_set", "can set"),)


class Tag(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название тега')
    slug = models.SlugField(max_length=255, verbose_name='URL', unique=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('python_exercise:tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ('name',)


# class Commentary(models.Model):
#     author = models.ForeignKey(
#         User, on_delete=models.CASCADE, null=False, verbose_name='Пользователь')
#     commentary_text = models.TextField(verbose_name='Комментарий')
#     time_create = models.DateTimeField(
#         verbose_name='Дата и время создания', auto_now_add=True)
#     exercise = models.ForeignKey(
#         'Exercise', on_delete=models.CASCADE, null=False, verbose_name='Задача')

#     def __str__(self):
#         return self.id

#     def get_absolute_url(self):
#         return reverse('commentary', kwargs={'commentary_id': self.id})

#     class Meta:
#         verbose_name = 'Комментарий'
#         verbose_name_plural = 'Комментарии'
#         ordering = ('id',)


class Place(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=255)


class Restaurant(Place):
    serves_hot_dogs = models.BooleanField(default=False)
    serves_pizza = models.BooleanField(default=False)

    
