# Generated by Django 3.2.16 on 2023-03-30 11:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_projecttypeproject_unique_project_type'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projecttypeproject',
            name='project',
        ),
        migrations.RemoveField(
            model_name='projecttypeproject',
            name='type',
        ),
        migrations.RemoveField(
            model_name='project',
            name='types',
        ),
        migrations.DeleteModel(
            name='ProjectType',
        ),
        migrations.DeleteModel(
            name='ProjectTypeProject',
        ),
    ]
