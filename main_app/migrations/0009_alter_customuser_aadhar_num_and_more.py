# Generated by Django 4.1.5 on 2023-01-26 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0008_customuser_aadhar_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='aadhar_num',
            field=models.IntegerField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='phone_num',
            field=models.IntegerField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='aadhar_num',
            field=models.IntegerField(max_length=12, null=True),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_num',
            field=models.IntegerField(max_length=12, null=True),
        ),
    ]
