# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2018-07-26 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0004_auto_20180726_1715'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='img',
            field=models.ImageField(blank=True, default='default.png', upload_to=''),
        ),
    ]