# Generated by Django 4.1.5 on 2023-02-03 06:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0022_remove_staff_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='staff',
            name='course',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.course'),
        ),
    ]
