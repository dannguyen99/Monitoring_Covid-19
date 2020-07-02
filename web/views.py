from datetime import datetime
import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import JhuData, VnData, EcdcData

# Create your views here.


def index(request):
    csvFile = pd.read_csv(JhuData.objects.last().csvFile)
    country = csvFile.groupby(['Country_Region']).sum().reset_index().sort_values(by= 'Confirmed', ascending=False)
    data_arr = country.to_numpy()[:, [0, 5]].tolist()
    countryTable = country.to_numpy()[:, [0, 5, 6, 7, 8]]
    context = {
        "countries": countryTable,
        "table": json.dumps(data_arr)
    }
    return render(request, 'web/index.html', context)


def vietNamView(request):
    rows = []
    sexs = []
    for d in VnData.objects.all().order_by('date'):
        csvFile = pd.read_csv(d.csvFile)
        if d.dataType == "PT":
            age_csv = csvFile
            sex = []
            stats = csvFile.groupby(
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
            row = []
            row.append(datetime.strftime(d.date, '%d/%m'))
            row.append(int(csvFile['Total cases'].sum()))
            row.append(int(csvFile['Death'].sum()))
            row.append(int(csvFile['Active'].sum()))
            row.append(int(csvFile['Recovered'].sum()))
            rows.append(row)
    ages = pd.concat([age_csv['Patient number'],
                      age_csv['Age']], axis=1).to_numpy().tolist()
    summary = rows[-1]
    context = {
        "ages": json.dumps(ages),
        "rows": json.dumps(rows),
        "sexs": json.dumps(sexs),
        "summary": summary
    }
    return render(request, 'web/vn_view.html', context)


def test(request):
    ecdc = pd.read_csv('data/ECDC/05-19-2020.csv')
    datas = EcdcData.objects.all()
    context = {
        'datas': datas,
        'ecdc':ecdc
    }
    return render(request, 'web/test.html', context)
