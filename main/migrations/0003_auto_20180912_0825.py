# Generated by Django 2.1.1 on 2018-09-12 08:25

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_overlap'),
    ]

    operations = [
        migrations.AlterField(
            model_name='overlap',
            name='partners',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=400), size=None),
        ),
    ]
