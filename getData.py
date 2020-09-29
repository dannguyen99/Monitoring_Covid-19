from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pandas as pd
import os
import django
import logging
import time
import requests
import json
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s ; %(name)s ; %(levelname)s ; %(message)s', level=logging.INFO,
                    datefmt="%Y-%m-%d %H:%M:%S")

os.environ['DJANGO_SETTINGS_MODULE'] = 'covid19.settings'
django.setup()
from web.models import JhuData, VnData, EcdcData, WhoData


def get_data_jhu():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    today = datetime.strftime(datetime.now(), '%m-%d-%Y')
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                           "/csse_covid_19_daily_reports/%s.csv" % yesterday)
        filePath = 'data/JHU/%s.csv' % today
        data.to_csv(filePath)
        insertJhuData(filePath)
        logging.info("Successfully updated data from JHU on %s" % today)
    except Exception as e:
        logging.error(e)


# get data from European Centre for Disease Prevention and Control ( EU )
def get_data_ecdc():
    today = datetime.strftime(datetime.now(), '%m-%d-%Y')
    data = pd.read_csv(
        "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    filePath = 'data/ECDC/%s.csv' % today
    data.to_csv(filePath)
    logging.info("Successfully updated data from ECDC on %s" % today)
    insertEcdcData(filePath)


def get_data_who():
    today = datetime.strftime(datetime.now(), '%m-%d-%Y')
    data = pd.read_csv(
        "https://covid19.who.int/WHO-COVID-19-global-data.csv")
    filePath = 'data/WHO/%s.csv' % today
    data.to_csv(filePath)
    logging.info("Successfully updated data from WHO on %s" % today)
    insertWhoData(filePath)


def get_data_vn():
    today = datetime.strftime(datetime.now(), '%m-%d-%Y')
    req = requests.get('https://ncov.moh.gov.vn/', verify=False)
    soup = BeautifulSoup(req.text, "html.parser")
    link_list = soup.findAll('a', {'class': "text-muted"})
    patients = []
    for link in link_list:
        onclick = link.get('onclick')
        case = onclick[16:-2]
        json_response = requests.get('https://ncov.moh.gov.vn/vi/web/guest/trang-chu?p_p_id=corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getThongTinDichTe&p_p_cacheability=cacheLevelPage&_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v_strValue=' + case, verify=False).text
        json_object = json.loads(json_response)
        patients.append(json_object)
    df = pd.json_normalize(patients)
    df.columns = ['patient_number', 'status', 'gender',
                  'city', 'description', 'age', 'classCss']
    req = requests.get('https://ncov.moh.gov.vn/', verify=False)
    soup = BeautifulSoup(req.text, "html.parser")
    table_rows = soup.find_all('tr')
    nationality_serie = pd.Series(row.find_all('td')[-1].text for row in table_rows[1:])
    df = df.assign(nationality=nationality_serie)
    filePath = 'data/VN/%s.csv' % today
    df.to_csv(filePath)
    logging.info("Successfully updated data from VN on %s" % today)
    insertVnData(filePath)


def collect_data():
    get_data_jhu()
    get_data_ecdc()
    get_data_vn()
    get_data_who()


def insertVnData(filePath):
    dtype = "PT"
    today = datetime.now()
    VnData.objects.filter(date=today, data_type=dtype).delete()
    data = VnData(data_type=dtype, date=today, csv_file=filePath)
    data.save()


def insertJhuData(filePath):
    today = datetime.now()
    JhuData.objects.filter(date=today).delete()
    data = JhuData(date=today, csv_file=filePath)
    data.save()


def insertEcdcData(filePath):
    today = datetime.now()
    EcdcData.objects.filter(date=today).delete()
    data = EcdcData(date=today, csv_file=filePath)
    data.save()


def insertWhoData(filePath):
    today = datetime.now()
    WhoData.objects.filter(date=today).delete()
    data = WhoData(date=today, csv_file=filePath)
    data.save()


collect_data()
