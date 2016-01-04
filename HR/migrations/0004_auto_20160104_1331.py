# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-01-04 08:01
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HR', '0003_auto_20160103_1829'),
    ]

    operations = [
        migrations.CreateModel(
            name='appSettingField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('name', models.CharField(max_length=50, unique=True)),
                ('flag', models.BooleanField(default=False)),
                ('value', models.CharField(max_length=50, null=True)),
                ('discription', models.CharField(max_length=500)),
                ('security', models.CharField(choices=[(b'admin', b'admin'), (b'staff', b'staff'), (b'owner', b'owner')], default=b'admin', max_length=5)),
                ('app', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='settings', to='HR.application')),
            ],
        ),
        migrations.AlterField(
            model_name='designation',
            name='unitType',
            field=models.CharField(choices=[(b'Not selected..', b'Not selected..'), (b'Research and Development', b'Research and Development'), (b'Operational', b'Operational'), (b'Management', b'Management')], default=b'Not selected..', max_length=30),
        ),
    ]
