# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-16 04:47
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('payroll', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='payslip',
            name='deffered',
            field=models.BooleanField(default=False),
        ),
    ]