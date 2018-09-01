# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-07-11 05:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0025_auto_20180711_0401'),
    ]

    operations = [
        migrations.CreateModel(
            name='Promocode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(max_length=100)),
                ('endDate', models.DateTimeField()),
                ('discount', models.IntegerField()),
                ('validTimes', models.IntegerField()),
            ],
        ),
    ]