# Generated by Django 4.0.2 on 2022-02-24 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Link',
            fields=[
                ('short_name', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='Короткое имя')),
                ('full_url', models.CharField(max_length=200, verbose_name='Полная ссылка')),
            ],
        ),
    ]
