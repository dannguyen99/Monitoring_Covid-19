from datetime import datetime
import json
import pandas as pd
import numpy as np
from django.http import HttpResponse, Http404, JsonResponse
from django.shortcuts import render
from.models import JhuData, VnData, EcdcData

# Create your views here.

# render index.html


def index(request):
    csv_file = pd.read_csv(JhuData.objects.last().csv_file)
    jhu_df = JhuData.index_table()
    summary = jhu_df.sum().to_numpy()[5:14]
    data_arr = jhu_df.dropna().to_numpy()[:, [0, 12]].tolist()
    countryTable = jhu_df.to_numpy()[:, [0, 5, 6, 7, 8, 11, 12, 13, 14]]
    daily_data = EcdcData.index_daily_cases_chart()
    daily_cases = daily_data[:, [0, 1]].tolist()
    daily_deaths = daily_data[:, [0, 2]].tolist()
    context = {
        "daily_deaths_data": daily_deaths,
        "daily_cases_data": daily_cases,
        "summary": summary,
        "countries": countryTable,
        "geochart_data": data_arr
    }
    return render(request, 'web/index.html', context)


def change_world_map(request):
    try:
        jhu_df = JhuData.index_table()
        filter_type = request.GET['filter_type']
        geochart_data = jhu_df.dropna().to_numpy()
        if filter_type == "confirmed":
            geochart_data = geochart_data[:, [0, 5]]
        else:
            geochart_data = geochart_data[:, [0, 12]]
        geochart_data = json.dumps(geochart_data.tolist())
        return JsonResponse({"success": True, "geochart_data": geochart_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})

# vietnam view


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
            sexs.append(sex)
    ages = pd.concat([age_csv['Patient number'],
                      age_csv['Age']], axis=1).to_numpy().tolist()
    summary = pd.read_csv(VnData.objects.filter(data_type="CT").order_by(
        'date').last().csv_file).sum().to_numpy()

    cities_geomap = VnData.cities_geomap()
    cities_summary = VnData.cities_summary()
    context = {
        "ages": json.dumps(ages),
        "sexs": json.dumps(sexs),
        "summary": summary,
        "cities_summary": cities_summary,
        "cities_geomap": cities_geomap
    }
    return render(request, 'web/vn_view.html', context)

# vietnam api


def vietnam_view_api(request):
    try:
        key = request.GET['key']
        if key == "daily_data":
            filter_type = request.GET['filter_type']
            cases, actives = VnData.vietnam_daily()
            if filter_type == "cases":
                daily_data = cases
            else:
                daily_data = actives
            return JsonResponse({"success": True, "data": daily_data})
    except Exception as e:
        return JsonResponse({"success": False, "message": str(e)})


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


def country_view(request, geoId):
    if EcdcData.get_country(geoId) is None:
        raise Http404("Country does not exist")
    cases, deaths, time_line, pop_2019 = EcdcData.get_country(geoId)
    cases_per_100k = round(cases/pop_2019 * 1000000, 2)
    summary = [cases, deaths, pop_2019, cases_per_100k]
    context = {
        "summary": summary,
        "time_line": time_line,
        "name": geoId
    }
    return render(request, 'web/country_view.html', context)


def test(request):
    ecdc = pd.read_csv('data/ECDC/05-19-2020.csv')
    datas = EcdcData.objects.all()
    cities_csv = VnData.cities_geomap()
    context = {
        'datas': datas,
        'ecdc': ecdc
    }
    return render(request, 'web/test.html', context)
