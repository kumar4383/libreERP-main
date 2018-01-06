# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-28 22:01
from __future__ import unicode_literals

from django.db import migrations, models
import products.models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0002_product_serial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('ticketID', models.PositiveIntegerField()),
                ('description', models.FileField(upload_to=products.models.getProductDP)),
            ],
        ),
    ]
