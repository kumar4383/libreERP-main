# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-08-08 09:41
from __future__ import unicode_literals

from django.db import migrations, models
import ecommerce.models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0042_auto_20180807_0639'),
    ]

    operations = [
        migrations.AddField(
            model_name='genericproduct',
            name='bannerImage',
            field=models.ImageField(null=True, upload_to=ecommerce.models.getEcommerceGenericProductBannerUploadPath),
        ),
    ]
