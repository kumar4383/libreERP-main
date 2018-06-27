# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-22 06:51
from __future__ import unicode_literals

from django.db import migrations, models
import ecommerce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0002_auto_20180521_1448'),
    ]

    operations = [
        migrations.CreateModel(
            name='genericProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('minCost', models.PositiveIntegerField(default=0)),
                ('visual', models.ImageField(null=True, upload_to=ecommerce.models.getEcommerceProductVisualUploadPath)),
                ('fields', models.ManyToManyField(blank=True, related_name='products', to='ecommerce.field')),
            ],
        ),
    ]
