# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 22:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0003_ticket'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.TextField(max_length=2000),
        ),
    ]
