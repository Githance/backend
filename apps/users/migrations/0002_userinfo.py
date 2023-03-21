# Generated by Django 3.2.16 on 2023-03-11 20:17

import apps.users.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=1000, null=True, verbose_name='О себе')),
                ('telegram', models.CharField(blank=True, max_length=32, null=True, validators=[django.core.validators.MinLengthValidator(5), apps.users.validators.validate_telegram_name], verbose_name='Телеграм')),
                ('portfolio_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на портфолио')),
                ('summary_url', models.URLField(blank=True, null=True, verbose_name='Ссылка на резюме')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_info', to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
        ),
    ]