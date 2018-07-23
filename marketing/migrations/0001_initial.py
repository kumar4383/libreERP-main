# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-05 08:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contacts',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('referenceId', models.CharField(blank=True, max_length=20, null=True)),
                ('name', models.CharField(blank=True, max_length=100, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('mobile', models.CharField(blank=True, max_length=12, null=True)),
                ('source', models.CharField(blank=True, max_length=20, null=True)),
                ('notes', models.TextField(blank=True, max_length=500, null=True)),
            ],
        ),
    ]