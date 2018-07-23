# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-05-01 15:03
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tools', '0004_documentcontent_text'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentSections',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('startPage', models.PositiveIntegerField()),
                ('endPage', models.PositiveIntegerField(null=True)),
                ('doc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tools.ArchivedDocument')),
            ],
        ),
    ]