# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-04-24 06:28
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('assets', '0004_allotment_checkin'),
    ]

    operations = [
        migrations.RenameField(
            model_name='asset',
            old_name='barcode',
            new_name='modelNo',
        ),
    ]
