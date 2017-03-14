from __future__ import unicode_literals

from django.db import models
from django.contrib.postgres.fields import JSONField

class Taxonomy(models.Model):
    """A model that handles the whole taxonomy"""
    data = JSONField()
    created = models.DateTimeField(auto_now_add=True)

    def get_root_node(self):
        parent = self.data[0]['id']
        child = None
        while parent:
            child = parent
            parent = self.get_one_parent(parent)
        return child

    def get_one_parent(self, ontology_id):
        for e in self.data:
            if ontology_id in e['child_ids']:
                return e['id']

    def get_children(self, ontology_id):
        for e in self.data:
            if e['id'] == ontology_id:
                return e['child_ids']
        return None

    def get_element_at_id(self, ontology_id):
        for e in self.data:
            if e['id'] == ontology_id:
                return e
        return None


class Sound(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    freesound_id = models.IntegerField()
    extra_data = JSONField(default={})

    def __str__(self):
        return 'Sound {0} (freesound {1})'.format(self.id, self.freesound_id)


class Dataset(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=200)
    short_name = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    taxonomy = JSONField(default={})
    sounds = models.ManyToManyField(Sound, related_name='datasets', through='datasets.SoundDataset')

    def __str__(self):
        return 'Dataset {0}'.format(self.name)


class SoundDataset(models.Model):
    sound = models.ForeignKey(Sound)
    dataset = models.ForeignKey(Dataset)


class Annotation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    sound_dataset = models.ForeignKey(SoundDataset, related_name='annotations')
    TYPE_CHOICES = (
        ('MA', 'Manual'),
        ('AU', 'Automatic'),
        ('UK', 'Unknown'),
    )
    type = models.CharField(max_length=2, choices=TYPE_CHOICES, default='UK')
    # TODO: add created_by property (user, can be null)
    algorithm = models.CharField(max_length=200, blank=True, null=True)
    value = models.CharField(max_length=200)
    start_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    end_time = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)

    def __str__(self):
        return 'Annotation for sound {0}'.format(self.sound_dataset.sound.id)


class Vote(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    # TODO: add created_by property (user)
    vote = models.IntegerField()
    annotation = models.ForeignKey(Annotation, related_name='votes')

    def __str__(self):
        return 'Vote for annotation {0}'.format(self.annotation.id)
