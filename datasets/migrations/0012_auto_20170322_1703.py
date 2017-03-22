# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-03-22 16:03
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0011_auto_20170322_1140'),
    ]

    operations = [
        migrations.AddField(
            model_name='datasetrelease',
            name='num_nodes',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='datasetrelease',
            name='release_tag',
            field=models.CharField(max_length=25, validators=[django.core.validators.RegexValidator(message='Please enter a valid release tag', regex='^[\\.a-zA-Z0-9_-]{1,25}$')]),
        ),
    ]
