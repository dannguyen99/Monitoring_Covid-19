import pandas as pd
from datetime import datetime, timedelta
import logging
import time
import requests
import csv
from bs4 import BeautifulSoup

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_data_jhu():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                           "/csse_covid_19_daily_reports/%s.csv" % yesterday)
        data.to_csv('data/JHU/%s.csv' % yesterday)
        logging.warning("Successfully updated data from JHU on %s" % yesterday)
    except Exception as e:
        logging.error(e)


# get data from European Centre for Disease Prevention and Control ( EU )
def get_data_ecdc():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    data = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    data.to_csv('data/ECDC/%s.csv' % yesterday)
    logging.warning("Successfully updated data from ECDC on %s" % yesterday)


def get_data_vn():
    req = requests.get('https://ncov.moh.gov.vn/', verify=False)
    soup = BeautifulSoup(req.text, "lxml")
    table_ncov = soup.find_all("table", {"class": "table table-striped table-covid19"})
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
        with open('data/VN/' + yesterday + '-' + name + '.csv', 'w') as csvfile:
            csvfile.write(header)
            writer = csv.writer(csvfile)
            writer.writerows(output_rows)
            logging.warning("Successfully updated data from VN on %s" % yesterday)


def collect_data():
    get_data_jhu()
    get_data_ecdc()
    get_data_vn()


# everyday do at 15 : 00 PM
#schedule.every().day.at("15:00").do(collect_data)
#while True:
#   schedule.run_pending()
#    time.sleep(60)  # wait one minute

collect_data()
