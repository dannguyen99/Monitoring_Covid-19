import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import Table, JhuData, VnData
from datetime import datetime

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
    for d in reversed(VnData.objects.all()):
        if d.data_type == "PT":
            continue
        row = []
        csv_file = pd.read_csv(d.csv_file)
        row.append(datetime.strftime(d.date, '%d/%m'))
        row.append(int(csv_file['Total cases'].sum()))
        row.append(int(csv_file['Death'].sum()))
        row.append(int(csv_file['Active'].sum()))
        row.append(int(csv_file['Recovered'].sum()))
        rows.append(row)
    context = {
        "rows": json.dumps(rows)
    }
    return render(request, 'web/vn_view.html', context)
