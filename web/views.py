import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import Table, JhuData

# Create your views here.


def index(request):
    csv_file = pd.read_csv(JhuData.objects.first().csv_file)
    country = csv_file.groupby(['Country_Region']).sum().reset_index()
    data_arr = country.to_numpy()[:, [0, 5]].tolist()
    print(data_arr)
    context = {
        "table": json.dumps(data_arr)
    }
    return render(request, 'web/index.html', context)