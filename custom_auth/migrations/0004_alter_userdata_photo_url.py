# Generated by Django 4.0.3 on 2022-04-04 09:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0003_userdata'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='photo_url',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Фотография'),
        ),
    ]
