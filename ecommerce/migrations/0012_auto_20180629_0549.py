# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-29 05:49
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0011_auto_20180629_0544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='genericproduct',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='ecommerce.genericProduct'),
        ),
    ]
