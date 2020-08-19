import os
import pandas as pd
import numpy as np

from datetime import datetime
from django.db import models
from django.utils import timezone
from django.conf import settings


# Create your models here.
country_dict = {"United_States_of_America": "US", "Saudi_Arabia": "Saudi Arabia", "Congo": "Congo (Kinshasa)", "Bosnia_and_Herzegovina": "Bosnia and Herzegovina",
                "United_Kingdom": "United Kingdom", "South_Africa": "South Africa",
                "United_Arab_Emirates": "United Arab Emirates", "Cote_dIvoire": "Cote d'Ivoire",
                "Dominican_Republic": "Dominican Republic", "South_Korea": "Korea, South", "El_Salvador": "El Salvador", "Costa_Rica": "Costa Rica", "North_Macedonia": "North Macedonia"}


class JhuData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/JHU')

    def __str__(self):
        return str(self.date)

    def index_table():
        csv_file = EcdcData.objects.order_by('date').last().csv_file
        ecdc_df = pd.read_csv(csv_file)
        ecdc_df = ecdc_df.groupby(
            'countriesAndTerritories').first().reset_index()
        ecdc_df = ecdc_df.replace({"countriesAndTerritories": country_dict})
        csv_file = JhuData.objects.order_by('date').last().csv_file
        jhu_df = pd.read_csv(csv_file)
        jhu_df = jhu_df.groupby('Country_Region').sum().reset_index()
        jhu_df['popData2019'] = jhu_df.Country_Region.map(
            ecdc_df.set_index('countriesAndTerritories')['popData2019'])
        jhu_df = jhu_df.dropna()
        jhu_df['casesPer1M'] = (jhu_df['Confirmed'] /
                                jhu_df['popData2019'] * 1000000).astype(int)
        jhu_df['new_cases'] = jhu_df.Country_Region.map(
            ecdc_df.set_index('countriesAndTerritories')['cases']).astype(int)
        jhu_df['new_deaths'] = jhu_df.Country_Region.map(
            ecdc_df.set_index('countriesAndTerritories')['deaths']).astype(int)
        jhu_df.Active = jhu_df.Active.astype(int)
        jhu_df.popData2019 = jhu_df.popData2019.astype(int)
        jhu_df = jhu_df.sort_values(by='Confirmed', ascending=False)
        return jhu_df

    def country_rate(country_name):
        csv_file = JhuData.objects.order_by('date').last().csv_file
        df = pd.read_csv(csv_file)
        df = df.groupby('Country_Region').mean().reset_index()
        df = df.loc[df['Country_Region'] == country_name].round(2).to_numpy()
        incidence_rate = df[0][9]
        case_fatality_ratio = df[0][10]
        return incidence_rate, case_fatality_ratio


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

    def vietnam_daily():
        cases = []
        actives = []
        for d in VnData.objects.filter(data_type="CT").order_by('date'):
            csv_file = pd.read_csv(d.csv_file)
            case = []
            active = []
            case.append(datetime.strftime(d.date, format='%Y,%m,%d'))
            active.append(datetime.strftime(d.date, format='%Y,%m,%d'))
            case.append(int(csv_file['Total cases'].sum()))
            case.append(int(csv_file['Recovered'].sum()))
            active.append(int(csv_file['Death'].sum()))
            active.append(int(csv_file['Active'].sum()))
            cases.append(case)
            actives.append(active)
        return cases, actives


class EcdcData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/ECDC')

    def get_country(country_name):
        csv_file = EcdcData.objects.order_by('date').last().csv_file
        df = pd.read_csv(csv_file)
        df['dateRep'] = pd.to_datetime(df.dateRep, format="%d/%m/%Y")
        df['dateRep'] = df.dateRep.dt.strftime('%Y,%m,%d')
        df = df.replace({"countriesAndTerritories": country_dict})
        country_df = df.loc[df['countriesAndTerritories'] == country_name]
        if country_df.any()['year'] == False:
            return
        else:
            cases = country_df.sum()['cases']
            deaths = country_df.sum()['deaths']
            time_line = np.flip(country_df.to_numpy()[:, [1, 5, 6]])
            pop_2019 = int(country_df.popData2019.iloc[0])
            return cases, deaths, time_line, pop_2019

    def index_daily_cases_chart():
        csv_file = EcdcData.objects.order_by('date').last().csv_file
        df = pd.read_csv(csv_file)
        df['dateRep'] = pd.to_datetime(df.dateRep, format="%d/%m/%Y")
        df = df.groupby('dateRep').sum().reset_index()
        df = df.sort_values(by='dateRep')
        begin = datetime(2020, 3, 13)
        df = df[(df['dateRep'] >= begin)]
        df['dateRep'] = df.dateRep.dt.strftime('%Y,%m,%d')
        data = df.to_numpy()[:, [0, 5, 6]]
        return data

    def __str__(self):
        return self.csv_file


class WhoData(models.Model):
    date = models.DateField()
    csv_file = models.FilePathField(path='data/WHO')
