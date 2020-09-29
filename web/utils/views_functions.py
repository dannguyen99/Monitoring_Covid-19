import pandas as pd
import numpy as np

from web.models import EcdcData, JhuData, VnData, WhoData
from datetime import datetime

country_dict = {"United_States_of_America": "US", "Saudi_Arabia": "Saudi Arabia", "Congo": "Congo (Kinshasa)",
                "Bosnia_and_Herzegovina": "Bosnia and Herzegovina",
                "United_Kingdom": "United Kingdom", "South_Africa": "South Africa",
                "United_Arab_Emirates": "United Arab Emirates", "Cote_dIvoire": "Cote d'Ivoire",
                "Dominican_Republic": "Dominican Republic", "South_Korea": "Korea, South", "El_Salvador": "El Salvador",
                "Costa_Rica": "Costa Rica", "North_Macedonia": "North Macedonia",
                "New_Zealand": "New Zealand", "Papua_New_Guinea": "Papua New Guinea",
                "Western_Sahara": "Western Sahara", "Sri_Lanka": "Sri Lanka"}


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


def country_rate(country_name):
    csv_file = JhuData.objects.order_by('date').last().csv_file
    df = pd.read_csv(csv_file)
    df = df.groupby('Country_Region').mean().reset_index()
    df = df.loc[df['Country_Region'] == country_name].round(2).to_numpy()
    incidence_rate = df[0][9]
    case_fatality_ratio = df[0][10]
    return incidence_rate, case_fatality_ratio


def world_summary():
    df = pd.read_csv(JhuData.objects.last().csv_file)
    data = df.sum()[['Recovered', 'Deaths', 'Active',
                     'Confirmed']].astype(int).tolist()
    data.insert(0, 0)
    df = pd.read_csv(WhoData.objects.last().csv_file)
    lasted_date = df.iloc[-1]['Date_reported']
    temp = df.loc[df['Date_reported'] == lasted_date][[
        ' New_cases', ' New_deaths']].sum().astype(int).tolist()
    data.append(temp[0])
    data.append(temp[1])
    temp = df[[' New_cases', ' New_deaths']].sum().astype(int).tolist()
    data[2] = temp[1]
    data[4] = temp[0]
    return data


def continent_cases(filter_type):
    df = pd.read_csv(EcdcData.objects.last().csv_file)
    if filter_type == 'total_cases':
        data = df.groupby('continentExp').cases.sum(
        ).reset_index().to_numpy().tolist()
        return data
    elif filter_type == 'new_cases':
        lasted_date = df.iloc[0]['dateRep']
        data = df.loc[df['dateRep'] == lasted_date].groupby(
            'continentExp').cases.sum().reset_index().to_numpy().tolist()
        return data


def get_country(country_name):
    csv_file = EcdcData.objects.order_by('date').last().csv_file
    df = pd.read_csv(csv_file)
    df['dateRep'] = pd.to_datetime(df.dateRep, format="%d/%m/%Y")
    df['dateRep'] = df.dateRep.dt.strftime('%Y,%m,%d')
    df = df.replace({"countriesAndTerritories": country_dict})
    country_df = df.loc[df['countriesAndTerritories'] == country_name]
    if not country_df.any()['year']:
        return
    else:
        cases = country_df.sum()['cases']
        deaths = country_df.sum()['deaths']
        time_line = np.flip(country_df.to_numpy()[:, [1, 5, 6]])
        pop_2019 = int(country_df.popData2019.iloc[0])
        return cases, deaths, time_line, pop_2019


def cities_geomap():
    cities = {"Hà Nội": "VN-HN", "Hồ Chí Minh": "VN-SG",
              "Bà Rịa - Vũng Tàu": "Bà Rịa-Vũng Tàu", "Đà Nẵng": "VN-DN",
              "Thừa Thiên Huế": "Thừa Thiên-Huế", "Hải Phòng": "Hải Phòng City",
              "Bạc Liêu": "VN-55", "Cần Thơ": "VN-`CT"}
    cities_csv = VnData.objects.filter(
        data_type="CT", date="2020-08-31").first().csv_file
    cities_arr = pd.read_csv(cities_csv).to_numpy()
    for c in cities_arr:
        city = c[0]
        if city in cities.keys():
            c[0] = cities[city]
    return cities_arr


def status_convertion(status):
    if status == "Khỏi":
        return 3
    elif status == "Đang điều trị":
        return 2
    elif status == "Tử vong":
        return 4
    else:
        return 5


def cities_summary():
    df = pd.read_csv(VnData.objects.last().csv_file)
    data = df.groupby(['city', 'status']).count().reset_index()[
        ['city', 'status', 'patient_number']].to_numpy()
    result = []
    for d in data:
        if len(result) == 0:
            temp = [d[0], 0, 0, 0, 0, 0]
            temp[status_convertion(d[1])] = d[2]
            temp[1] = sum(temp[2:])
            result.append(temp)
        elif result[len(result) - 1][0] == d[0]:
            result[len(result) - 1][status_convertion(d[1])] = d[2]
            result[len(result) - 1][1] = sum(result[len(result) - 1][2:])
        else:
            temp = [d[0], 0, 0, 0, 0, 0]
            temp[status_convertion(d[1])] = d[2]
            temp[1] = sum(temp[2:])
            result.append(temp)
    return result


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


def country_geomap():
    df = pd.read_csv(WhoData.objects.last().csv_file)
    data = df.groupby(' Country_code').sum(
    ).reset_index().to_numpy()[:, [0, 2]].tolist()
    return data


def who_region_new_cases():
    df = pd.read_csv(WhoData.objects.last().csv_file)
    df = df.groupby(' WHO_region')[
        [' WHO_region', ' New_cases']].sum().reset_index()
    data = df.to_numpy().tolist()
    return data


def case_ratio():
    df = pd.read_csv(JhuData.objects.last().csv_file)
    data = df[['Deaths', 'Recovered', 'Active']].sum().to_numpy()
    types = ['Death Cases', 'Recovered Cases', 'Active Cases']
    result = []
    for number, type in zip(data, types):
        result.append([type, number])
    return result


def vietnam_summary():
    records = VnData.objects.all().order_by('-date')
    today_record = records[0]
    prev_record = records[1]
    df = pd.read_csv(today_record.csv_file)
    prev_df = pd.read_csv(prev_record.csv_file)
    new_cases = len(df.index) - len(prev_df.index)
    new_deaths = df.groupby('status').count(
    ).age[2] - prev_df.groupby('status').count().age[2]
    data = df.groupby('status').count().patient_number.to_numpy().tolist()
    data.append(int(sum(data)))
    data.append(int(new_cases))
    data.append(int(new_deaths))
    return data


def vietnam_age():
    df = pd.read_csv(VnData.objects.last().csv_file)
    data = df[['patient_number', 'age']].to_numpy().tolist()
    return data


def vietnam_nationality():
    df = pd.read_csv(VnData.objects.last().csv_file)
    data = df.groupby('nationality').count().reset_index()[
        ['nationality', 'age']].to_numpy().tolist()
    return data


def vietnam_gender():
    df = pd.read_csv(VnData.objects.filter(data_type='PT').last().csv_file)
    data = df.groupby('gender')['patient_number'].nunique().tolist()
    return data
