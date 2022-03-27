# Generated by Django 4.0.3 on 2022-03-23 09:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Категория')),
                ('slug', models.SlugField(max_length=255, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Категория',
                'verbose_name_plural': 'Категории',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название тега')),
                ('slug', models.SlugField(max_length=255, unique=True, verbose_name='URL')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255, verbose_name='Название задачи')),
                ('task_text', models.TextField(verbose_name='Текст задачи')),
                ('is_published', models.BooleanField(default=True, verbose_name='Публикация')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата и время изменения')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='python_exercise.category', verbose_name='Категория')),
                ('tag', models.ManyToManyField(blank=True, to='python_exercise.tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Задача',
                'verbose_name_plural': 'Задачи',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentary_text', models.TextField(verbose_name='Комментарий')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
                ('exercise', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='python_exercise.exercise', verbose_name='Задача')),
            ],
            options={
                'verbose_name': 'Комментарий',
                'verbose_name_plural': 'Комментарии',
                'ordering': ('id',),
            },
        ),
    ]
