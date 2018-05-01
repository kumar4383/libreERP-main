# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-04-23 13:37
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import taskBoard.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('gitweb', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='media',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('link', models.TextField(max_length=300, null=True)),
                ('attachment', models.FileField(null=True, upload_to=taskBoard.models.getTaskUploadsPath)),
                ('mediaType', models.CharField(choices=[('onlineVideo', 'onlineVideo'), ('video', 'video'), ('image', 'image'), ('onlineImage', 'onlineImage'), ('doc', 'doc')], default='image', max_length=10)),
                ('name', models.CharField(max_length=100, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasksUploads', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='subTask',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('status', models.CharField(choices=[('notStarted', 'notStarted'), ('inProgress', 'inProgress'), ('stuck', 'stuck'), ('complete', 'complete')], default='notStarted', max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField(max_length=2000)),
                ('dueDate', models.DateTimeField()),
                ('personal', models.BooleanField(default=False)),
                ('completion', models.PositiveIntegerField(default=0)),
                ('archived', models.BooleanField(default=False)),
                ('files', models.ManyToManyField(blank=True, related_name='tasks', to='taskBoard.media')),
                ('followers', models.ManyToManyField(blank=True, related_name='taskFollowing', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
                ('to', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='timelineItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('category', models.CharField(choices=[('message', 'message'), ('git', 'git'), ('file', 'file'), ('system', 'system')], default='message', max_length=50)),
                ('text', models.TextField(max_length=2000, null=True)),
                ('commit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to='gitweb.commitNotification')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='taskBoard.task')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='subtask',
            name='task',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subTasks', to='taskBoard.task'),
        ),
        migrations.AddField(
            model_name='subtask',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
