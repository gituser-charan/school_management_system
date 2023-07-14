# Generated by Django 4.2.2 on 2023-07-06 07:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sms', '0006_staff_user_students_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='students',
            name='mothers_mobile_no',
            field=models.BigIntegerField(null=True, unique=True, validators=[django.core.validators.MaxValueValidator(9999999999), django.core.validators.MinValueValidator(0)]),
        ),
    ]
