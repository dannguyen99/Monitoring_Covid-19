import json
from datetime import datetime, date

import pandas as pd
import numpy as np
from django.http import Http404, JsonResponse
from django.shortcuts import render

from .models import JhuData, VnData, EcdcData
from .utils import views_functions


# Create your views here.

# render index.html
def index(request):
    jhu_df = views_functions.index_table()
    summary = views_functions.world_summary()
    data_arr = jhu_df.dropna().to_numpy()[:, [0, 12]].tolist()
    country_table = jhu_df.to_numpy()[:, [0, 5, 6, 7, 8, 11, 12, 13, 14]]
    daily_data = views_functions.index_daily_cases_chart()
    daily_cases = daily_data[:, [0, 1]].tolist()
    daily_deaths = daily_data[:, [0, 2]].tolist()
    context = {
        "daily_deaths_data": daily_deaths,
        "daily_cases_data": daily_cases,
        "summary": summary,
        "countries": country_table,
        "geochart_data": data_arr
    }
    return render(request, 'web/index.html', context)


def last_update(request):
    try:
        with open('app.log', 'r') as log_file:
            lines = log_file.read().splitlines()
            time = lines[-1].split(';')[0]
            last_update = datetime.strptime(time, "%Y-%m-%d %H:%M:%S ")
            last_update = datetime.strftime(last_update, "%Y-%m-%dT%H:%M:%S")
            return JsonResponse({"success": True, "last_update": last_update})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


# vietnam view


def vietnam_view(request):
    summary = views_functions.vietnam_summary()
    cities_summary = views_functions.cities_summary()
    context = {
        "summary": summary,
        "cities_summary": cities_summary,
        "patient_summary": views_functions.patient_summary()
    }
    return render(request, 'web/vn_view.html', context)


def visualization(request):
    csv_file = pd.read_csv(JhuData.objects.last().csv_file)
    country = csv_file.groupby(['Province_State']).sum(
    ).reset_index().sort_values(by='Confirmed', ascending=False)
    data_arr = country.to_numpy()[:, [0, 5, 6, 7, 8]].tolist()
    context = {
        "states": data_arr
    }
    return render(request, 'web/visualization.html', context)


def country_view(request, geoId):
    if views_functions.get_country(geoId) is None:
        raise Http404("Country does not exist")
    cases, deaths, time_line, pop_2019 = views_functions.get_country(geoId)
    cases_per_100k = round(cases / pop_2019 * 1000000, 2)
    incidence_rate, case_fatality_ratio = views_functions.country_rate(geoId)
    summary = [cases, deaths, pop_2019, cases_per_100k,
               incidence_rate, case_fatality_ratio]
    context = {
        "summary": summary,
        "time_line": time_line,
        "name": geoId
    }
    return render(request, 'web/country_view.html', context)


def references(request):
    return render(request, 'web/references.html')


def about(request):
    return render(request, 'web/about.html')


def test(request):
    data = views_functions.country_geomap()
    context = {
        "data": data
    }
    return render(request, 'web/test.html', context)
