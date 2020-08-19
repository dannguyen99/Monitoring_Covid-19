import pandas as pd
import os
import django
import logging
import time
import requests
import csv

from datetime import datetime, timedelta
from bs4 import BeautifulSoup

logging.basicConfig(filename='app.log', filemode='a',
                    format='%(asctime)s ; %(name)s ; %(levelname)s ; %(message)s', level=logging.INFO, datefmt="%Y-%m-%d %H:%M:%S")

os.environ['DJANGO_SETTINGS_MODULE'] = 'covid19.settings'
django.setup()

from web.models import JhuData, VnData, EcdcData, WhoData

def get_data_jhu():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                           "/csse_covid_19_daily_reports/%s.csv" % yesterday)

        filePath = 'data/JHU/%s.csv' % yesterday
        data.to_csv(filePath)
        insertJhuData(filePath)
        logging.info("Successfully updated data from JHU on %s" % yesterday)
    except Exception as e:
        logging.error(e)


# get data from European Centre for Disease Prevention and Control ( EU )
def get_data_ecdc():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    data = pd.read_csv(
        "https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    filePath = 'data/ECDC/%s.csv' % yesterday
    data.to_csv(filePath)
    logging.info("Successfully updated data from ECDC on %s" % yesterday)
    insertEcdcData(filePath)


def get_data_who():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    data = pd.read_csv(
        "https://covid19.who.int/WHO-COVID-19-global-data.csv")
    filePath = 'data/WHO/%s.csv' % yesterday
    data.to_csv(filePath)
    logging.info("Successfully updated data from WHO on %s" % yesterday)
    insertWhoData(filePath)


def get_data_vn():
    req = requests.get('https://ncov.moh.gov.vn/', verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    table_ncov = soup.find_all(
        "table", {"class": "table table-striped table-covid19"})
    headers = ["City,Total cases,Active,Recovered,Death",
               "Patient number,Age,Gender,Location,Status,Nationality"]
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    names = ["cities", "patients"]
    for table, header, name in zip(table_ncov, headers, names):
        output_rows = []
        for table_row in table.findAll('tr'):
            columns = table_row.findAll('td')
            output_row = []
            for column in columns:
                output_row.append(column.text)
            output_rows.append(output_row)
        filePath = 'data/VN/' + yesterday + '-' + name + '.csv'
        with open(filePath, 'w', encoding="utf-8") as csv_file:
            csv_file.write(header)
            writer = csv.writer(csv_file)
            writer.writerows(output_rows)
            logging.info(
                "Successfully updated data from VN on %s" % yesterday)
            insertVnData(filePath, name)


def collect_data():
    get_data_jhu()
    get_data_ecdc()
    get_data_vn()
    get_data_who()


def insertVnData(filePath, data_type):
    if data_type == "cities":
        dtype = "CT"
    else:
        dtype = "PT"
    yesterday = datetime.now() - timedelta(1)
    VnData.objects.filter(date=yesterday, data_type=dtype).delete()
    data = VnData(data_type=dtype, date=yesterday, csv_file=filePath)
    data.save()


def insertJhuData(filePath):
    yesterday = datetime.now() - timedelta(1)
    JhuData.objects.filter(date=yesterday).delete()
    data = JhuData(date=yesterday, csv_file=filePath)
    data.save()

    yesterday = datetime.now() - timedelta(1)


def insertEcdcData(filePath):
    yesterday = datetime.now() - timedelta(1)
    EcdcData.objects.filter(date=yesterday).delete()
    data = EcdcData(date=yesterday, csv_file=filePath)
    data.save()


def insertWhoData(filePath):
    yesterday = datetime.now() - timedelta(1)
    WhoData.objects.filter(date=yesterday).delete()
    data = WhoData(date=yesterday, csv_file=filePath)
    data.save()


collect_data()
