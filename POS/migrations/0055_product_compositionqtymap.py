# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-26 17:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('POS', '0054_auto_20180626_1703'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='compositionQtyMap',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]