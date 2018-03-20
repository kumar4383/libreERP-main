# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-08 08:41
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('warehouse', '0012_auto_20180226_0628'),
    ]

    operations = [
        migrations.CreateModel(
            name='Checkin',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('description', models.CharField(max_length=10000)),
                ('height', models.PositiveIntegerField(null=True)),
                ('width', models.PositiveIntegerField(null=True)),
                ('length', models.PositiveIntegerField(null=True)),
                ('weight', models.PositiveIntegerField(null=True)),
                ('checkedin', models.BooleanField(default=True)),
                ('contract', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='checkins', to='warehouse.Contract')),
            ],
        ),
    ]