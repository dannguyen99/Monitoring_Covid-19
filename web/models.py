import os

import pandas as pd
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

    def cities_geomap():
        cities = {"Hà Nội": "VN-HN", "Hồ Chí Minh": "VN-SG", 
        "Bà Rịa - Vũng Tàu": "Bà Rịa-Vũng Tàu", "Đà Nẵng": "VN-DN", 
        "Thừa Thiên Huế": "Thừa Thiên-Huế", "Hải Phòng": "Hải Phòng City"}
        cities_csv = VnData.objects.filter(data_type = "CT").order_by('date').last().csv_file
        cities_arr = pd.read_csv(cities_csv).to_numpy()
        for c in cities_arr:
            city = c[0]
            if city in cities.keys():
                c[0] = cities[city]
        return cities_arr

class EcdcData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/ECDC')

    def __str__(self):
        return self.csv_file
