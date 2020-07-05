from datetime import datetime
import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import JhuData, VnData, EcdcData

# Create your views here.


def index(request):
    csv_file = pd.read_csv(JhuData.objects.last().csv_file)
    country = csv_file.groupby(['Country_Region']).sum(
    ).reset_index().sort_values(by='Confirmed', ascending=False)
    data_arr = country.to_numpy()[:, [0, 5]].tolist()
    countryTable = country.to_numpy()[:, [0, 5, 6, 7, 8]]
    context = {
        "countries": countryTable,
        "table": json.dumps(data_arr)
    }
    return render(request, 'web/index.html', context)


def vietnam_view(request):
    rows = []
    sexs = []
    for d in VnData.objects.all().order_by('date'):
        csv_file = pd.read_csv(d.csv_file)
        if d.data_type == "PT":
            age_csv = csv_file
            sex = []
            stats = csv_file.groupby(
                'Gender')['Patient number'].nunique().to_numpy()
            male = int(stats[0])
            female = int(stats[1])
            total = male + female
            sex.append(datetime.strftime(d.date, '%d/%m'))
            sex.append(male)
            sex.append(female)
            sex.append(total)
            sexs.append(sex)
        else:
            cities_csv = csv_file
            row = []
            row.append(datetime.strftime(d.date, '%d/%m'))
            row.append(int(csv_file['Total cases'].sum()))
            row.append(int(csv_file['Death'].sum()))
            row.append(int(csv_file['Active'].sum()))
            row.append(int(csv_file['Recovered'].sum()))
            rows.append(row)
    ages = pd.concat([age_csv['Patient number'],
                      age_csv['Age']], axis=1).to_numpy().tolist()
    summary = rows[-1]
    cities = cities_csv.to_numpy()
    context = {
        "ages": json.dumps(ages),
        "rows": json.dumps(rows),
        "sexs": json.dumps(sexs),
        "summary": summary,
        "cities": cities
    }
    return render(request, 'web/vn_view.html', context)

def euView(request):
    return render(request, 'web/eu_view.html')

def us_view(request):
    csv_file = pd.read_csv(JhuData.objects.last().csv_file)
    country = csv_file.groupby(['Province_State']).sum(
    ).reset_index().sort_values(by='Confirmed', ascending=False)
    data_arr = country.to_numpy()[:, [0, 5, 6, 7, 8]].tolist()
    context = {
        "states": data_arr
    }
    return render(request, 'web/us_view.html', context)


def test(request):
    ecdc = pd.read_csv('data/ECDC/05-19-2020.csv')
    datas = EcdcData.objects.all()
    context = {
        'datas': datas,
        'ecdc': ecdc
    }
    return render(request, 'web/test.html', context)
