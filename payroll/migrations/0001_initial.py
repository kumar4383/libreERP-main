# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-03-15 10:24
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='PayrollReport',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('month', models.PositiveIntegerField()),
                ('year', models.PositiveIntegerField()),
                ('total', models.PositiveIntegerField(null=True)),
                ('totalTDS', models.PositiveIntegerField(null=True)),
                ('status', models.CharField(choices=[('created', 'created'), ('submitted', 'submitted'), ('approved', 'approved'), ('processed', 'processed'), ('reconciled', 'reconciled')], default='created', max_length=30)),
                ('dateOfProcessing', models.DateField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payrollReportsCreated', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payslip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateField(auto_now=True)),
                ('adHoc', models.PositiveIntegerField(default=0)),
                ('month', models.PositiveIntegerField()),
                ('year', models.PositiveIntegerField()),
                ('tds', models.PositiveIntegerField()),
                ('days', models.PositiveIntegerField()),
                ('report', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to='payroll.PayrollReport')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payslips', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AlterUniqueTogether(
            name='payslip',
            unique_together=set([('year', 'month', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='payrollreport',
            unique_together=set([('year', 'month')]),
        ),
    ]
