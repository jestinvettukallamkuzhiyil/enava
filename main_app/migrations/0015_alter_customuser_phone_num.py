# Generated by Django 4.1.5 on 2023-01-30 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0014_alter_customuser_aadhar_num'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='phone_num',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
