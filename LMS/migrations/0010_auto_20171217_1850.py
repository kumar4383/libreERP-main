# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-12-17 18:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('LMS', '0009_auto_20171217_1847'),
    ]

    operations = [
        migrations.RenameField(
            model_name='enrollment',
            old_name='couse',
            new_name='course',
        ),
    ]
