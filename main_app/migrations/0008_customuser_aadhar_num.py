# Generated by Django 4.1.5 on 2023-01-26 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0007_alter_student_aadhar_num'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='aadhar_num',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
