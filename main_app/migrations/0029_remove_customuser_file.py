# Generated by Django 4.1.5 on 2023-02-19 15:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0028_customuser_file'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='file',
        ),
    ]
