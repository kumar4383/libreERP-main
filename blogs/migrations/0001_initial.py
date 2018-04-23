# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('PIM', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='blogBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bookmarks', to='PIM.blogPost')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blogsBookmarked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
