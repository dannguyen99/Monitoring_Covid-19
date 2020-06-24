from datetime import datetime
import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import Table, JhuData, VnData

# Create your views here.


def index(request):
    csv_file = pd.read_csv(JhuData.objects.first().csv_file)
    country = csv_file.groupby(['Country_Region']).sum().reset_index()
    data_arr = country.to_numpy()[:, [0, 5]].tolist()
    context = {
        "table": json.dumps(data_arr)
    }
    return render(request, 'web/index.html', context)


def vietNamView(request):
    rows = []
    sexs = []
    for d in VnData.objects.all().order_by('date'):
        csv_file = pd.read_csv(d.csv_file)
        if d.data_type == "PT":
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
            row = []
            row.append(datetime.strftime(d.date, '%d/%m'))
            row.append(int(csv_file['Total cases'].sum()))
            row.append(int(csv_file['Death'].sum()))
            row.append(int(csv_file['Active'].sum()))
            row.append(int(csv_file['Recovered'].sum()))
            rows.append(row)
    context = {
        "rows": json.dumps(rows),
        "sexs": json.dumps(sexs)
    }
    return render(request, 'web/vn_view.html', context)


def test(request):
    context = {}
    return render(request, 'web/test.html', context)
