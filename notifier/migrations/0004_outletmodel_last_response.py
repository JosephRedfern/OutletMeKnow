# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-30 23:22
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifier', '0003_auto_20170430_2313'),
    ]

    operations = [
        migrations.AddField(
            model_name='outletmodel',
            name='last_response',
            field=models.TextField(null=True),
        ),
    ]