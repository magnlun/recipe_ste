# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2016-05-31 07:00
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes_models', '0005_auto_20160531_0657'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quantity',
            name='comment',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
