import json
import pandas as pd
import numpy as np
from django.http import HttpResponse
from django.shortcuts import render
from.models import Table

# Create your views here.


def index(request):
    csv_file = pd.read_csv(Table.objects.first().csv_file)
    data_arr = csv_file.to_numpy()[:, [4, 8]].tolist()
    context = {
        "table": json.dumps(data_arr)
    }
    return render(request, 'web/index.html', context)
