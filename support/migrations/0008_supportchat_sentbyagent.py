# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-08 08:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('support', '0007_auto_20180807_1254'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportchat',
            name='sentByAgent',
            field=models.BooleanField(default=False),
        ),
    ]
