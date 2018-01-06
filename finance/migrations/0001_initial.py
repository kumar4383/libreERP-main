# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2017-09-12 17:58
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import finance.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('ERP', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('number', models.PositiveIntegerField()),
                ('ifsc', models.CharField(max_length=15)),
                ('bank', models.CharField(max_length=50)),
                ('bankAddress', models.TextField(max_length=500)),
                ('personal', models.BooleanField(default=False)),
                ('authorizedSignaturies', models.ManyToManyField(related_name='checkingAccounts', to=settings.AUTH_USER_MODEL)),
                ('contactPerson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accountsManaging', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CostCenter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('code', models.CharField(max_length=50)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='finance.Account')),
                ('head', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('projects', models.ManyToManyField(related_name='costCenters', to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='ExpenseSheet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('approved', models.BooleanField(default=False)),
                ('approvalMatrix', models.PositiveSmallIntegerField(default=1)),
                ('approvalStage', models.PositiveSmallIntegerField(default=0)),
                ('dispensed', models.BooleanField(default=False)),
                ('notes', models.TextField(max_length=500, null=True)),
                ('submitted', models.BooleanField(default=False)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.project')),
            ],
        ),
        migrations.CreateModel(
            name='Inflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('ammount', models.PositiveIntegerField()),
                ('referenceID', models.CharField(max_length=30)),
                ('currency', models.CharField(choices=[('INR', 'INR'), ('USD', 'USD')], max_length=5)),
                ('dated', models.DateField()),
                ('attachment', models.FileField(null=True, upload_to=finance.models.getInflowAttachmentsPath)),
                ('description', models.TextField(max_length=200)),
                ('verified', models.BooleanField(default=False)),
                ('fromBank', models.CharField(max_length=30, null=True)),
                ('chequeNo', models.CharField(max_length=30, null=True)),
                ('mode', models.CharField(choices=[('cash', 'cash'), ('cheque', 'cheque'), ('wire', 'wire')], default='cash', max_length=20)),
                ('balance', models.PositiveIntegerField()),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='inflow', to='ERP.service')),
                ('toAcc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inflowCredits', to='finance.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inflowsTransacted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('amount', models.PositiveIntegerField(default=0)),
                ('currency', models.CharField(choices=[('INR', 'INR'), ('USD', 'USD')], max_length=5)),
                ('dated', models.DateField()),
                ('attachment', models.FileField(null=True, upload_to=finance.models.getInvoicesPath)),
                ('description', models.TextField(max_length=200)),
                ('approved', models.BooleanField(default=False)),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ERP.service')),
                ('sheet', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoices', to='finance.ExpenseSheet')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invoiceGeneratedOrSubmitted', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ammount', models.PositiveIntegerField()),
                ('balance', models.PositiveIntegerField()),
                ('externalReferenceID', models.CharField(max_length=30)),
                ('externalConfirmationID', models.CharField(max_length=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('api', models.CharField(max_length=20)),
                ('apiCallParams', models.CharField(max_length=1500)),
                ('fromAcc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='debits', to='finance.Account')),
                ('toAcc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='credits', to='finance.Account')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transactions', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='expensesheet',
            name='transaction',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expenseSheet', to='finance.Transaction'),
        ),
        migrations.AddField(
            model_name='expensesheet',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expenseGeneratedOrSubmitted', to=settings.AUTH_USER_MODEL),
        ),
    ]
