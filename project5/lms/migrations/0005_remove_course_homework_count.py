# Generated by Django 4.0.5 on 2022-07-12 09:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0004_alter_homework_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='course',
            name='homework_count',
        ),
    ]
