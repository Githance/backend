# Generated by Django 3.2.16 on 2023-03-30 11:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20230328_0047'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='projecttypeproject',
            name='unique_project_type',
        ),
    ]