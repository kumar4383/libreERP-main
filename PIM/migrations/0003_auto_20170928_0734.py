# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-28 07:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('PIM', '0002_auto_20170928_0724'),
    ]

    operations = [
        migrations.AlterField(
            model_name='calendar',
            name='level',
            field=models.CharField(choices=[(b'Normal', b'Normal'), (b'Critical', b'Critical'), (b'Optional', b'Optional'), (b'Mandatory', b'Mandatory')], default=b'Normal', max_length=10),
        ),
    ]
