# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-01-23 06:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0002_auto_20180122_2353'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='company',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='contacts', to='warehouse.Service'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='contact',
            name='designation',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='email',
            field=models.EmailField(max_length=254, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='mobile',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='contact',
            name='notes',
            field=models.TextField(max_length=300, null=True),
        ),
    ]
