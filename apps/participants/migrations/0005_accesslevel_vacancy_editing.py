# Generated by Django 3.2.16 on 2023-05-08 21:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('participants', '0004_auto_20230330_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='accesslevel',
            name='vacancy_editing',
            field=models.BooleanField(default=False, verbose_name='Право редактирования вакансий'),
        ),
    ]
