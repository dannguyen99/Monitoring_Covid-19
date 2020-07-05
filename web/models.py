import os

from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.
class JhuData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/JHU')

    def __str__(self):
        return str(self.date)


class VnData(models.Model):
    TYPE_CHOICES = [
        ('CT', 'CITIES'),
        ('PT', 'PATIENTS')
    ]
    data_type = models.CharField(
        max_length=2, choices=TYPE_CHOICES, default='CITIES')
    date = models.DateField()
    csv_file = models.FilePathField(path='data/VN')

    def __str__(self):
        return "%s %s" % (self.data_type, str(self.date))


class EcdcData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/ECDC')

    def __str__(self):
        return self.csv_file
