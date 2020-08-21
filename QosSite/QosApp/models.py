from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Table(models.Model):
    id = models.AutoField(primary_key=True)
    flow = models.CharField(default='', max_length=512)
    flow_node = models.CharField(default='', max_length=256)
    priority = models.CharField(default='', max_length=128)
    inport = models.CharField(default='', max_length=64)
    match = models.CharField(max_length=1024)
    instruction = models.CharField(max_length=1024)


class Meter(models.Model):
    id = models.AutoField(primary_key=True)
    meter = models.CharField(max_length=256)
    meterType = models.CharField(max_length=256)
    bandRate = models.CharField(max_length=256)
    bandSize = models.CharField(max_length=256)
