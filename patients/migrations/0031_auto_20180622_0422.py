# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-22 04:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0030_auto_20180622_0412'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='dischargesummary',
            name='doctorName',
        ),
        migrations.RemoveField(
            model_name='dischargesummary',
            name='regNo',
        ),
        migrations.AddField(
            model_name='dischargesummary',
            name='summaryKeyInvestigation',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
