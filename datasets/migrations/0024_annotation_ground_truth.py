# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-06 10:17
from __future__ import unicode_literals

from django.db import migrations, models
from django.db import transaction


def add_ground_truth(apps, schema_editor):
    Annotation = apps.get_model('datasets', 'Annotation')
    all_annotations = Annotation.objects.all()
    for annotation in all_annotations:
        vote_values = [v.vote for v in annotation.votes.all()]
        if vote_values.count(1) > 1:
            annotation.ground_truth = 1
        if vote_values.count(0.5) > 1:
            annotation.ground_truth = 0.5
        if vote_values.count(0) > 1:
            annotation.ground_truth = 0
        if vote_values.count(-1) > 1:
            annotation.ground_truth = -1
        annotation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('datasets', '0023_auto_20170623_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='annotation',
            name='ground_truth',
            field=models.FloatField(blank=True, default=None, null=True),
        ),
        migrations.RunPython(add_ground_truth, migrations.RunPython.noop)
    ]