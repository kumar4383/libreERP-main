# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-06-15 07:23
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Patients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('age', models.PositiveIntegerField(null=True)),
                ('gender', models.CharField(max_length=100)),
                ('uniqueId', models.CharField(max_length=100)),
            ],
        ),
    ]
