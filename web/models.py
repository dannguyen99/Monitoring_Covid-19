import os

import pandas as pd
import numpy as np
from django.db import models
from django.utils import timezone
from django.conf import settings

# Create your models here.


class JhuData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/JHU')

    def __str__(self):
        return str(self.date)

    def index_table():
        csv_file = EcdcData.objects.order_by('date').last().csv_file
        ecdc_df = pd.read_csv(csv_file)
        ecdc_df = ecdc_df.groupby(
            'countriesAndTerritories').mean().popData2019.reset_index()
        csv_file = JhuData.objects.order_by('date').last().csv_file
        jhu_df = pd.read_csv(csv_file)
        jhu_df = jhu_df.groupby('Country_Region').sum().reset_index()
        jhu_df['popData2019'] = jhu_df.Country_Region.map(
            ecdc_df.set_index('countriesAndTerritories')['popData2019'])
        jhu_df['casesPer1M'] = jhu_df['Confirmed'] / \
            jhu_df['popData2019'] * 1000000
        jhu_df.sort_values(by='Confirmed', ascending=False)
        print(jhu_df.head())
        return jhu_df

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
                  "Thừa Thiên Huế": "Thừa Thiên-Huế", "Hải Phòng": "Hải Phòng City",
                  "Bạc Liêu": "VN-55", "Cần Thơ": "VN-`CT"}
        cities_csv = VnData.objects.filter(
            data_type="CT").order_by('date').last().csv_file
        cities_arr = pd.read_csv(cities_csv).to_numpy()
        for c in cities_arr:
            city = c[0]
            if city in cities.keys():
                c[0] = cities[city]
        return cities_arr

    def cities_summary():
        cities_csv = VnData.objects.filter(
            data_type="CT").order_by('date').last().csv_file
        cities_arr = pd.read_csv(cities_csv).to_numpy()
        return cities_arr


class EcdcData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/ECDC')

    def get_country(country_name):
        names = {"US": "United_States_of_America",
                 "United Kingdom": "United_Kingdom"}
        if country_name in names.keys():
            country_name = names[country_name]
        csv_file = EcdcData.objects.order_by('date').last().csv_file
        df = pd.read_csv(csv_file)
        country_df = df.loc[df['countriesAndTerritories'] == country_name]
        if country_df.any()['year'] == False:
            return
        else:
            cases = country_df.sum()['cases']
            deaths = country_df.sum()['deaths']
            time_line = np.flip(country_df.to_numpy()[:, [1, 5, 6]])
            pop_2019 = int(country_df.popData2019.iloc[0])
            return cases, deaths, time_line, pop_2019

    def __str__(self):
        return self.csv_file
