# Generated by Django 4.0.3 on 2022-03-25 10:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('python_exercise', '0002_exercise_author_create_exercise_author_update_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='exercise',
            options={'ordering': ('time_update',), 'verbose_name': 'Задача', 'verbose_name_plural': 'Задачи'},
        ),
    ]
