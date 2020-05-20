import pandas as pd
from datetime import datetime, timedelta
import logging
import schedule
import time

logging.basicConfig(filename='app.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


def get_data_jhu():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    try:
        data = pd.read_csv("https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data"
                           "/csse_covid_19_daily_reports/%s.csv" % yesterday)
        data.to_csv('data/JHU/%s.csv' % yesterday)
    except Exception as e:
        logging.error(e)


def get_data_ecdc():
    yesterday = datetime.strftime(datetime.now() - timedelta(1), '%m-%d-%Y')
    data = pd.read_csv("https://opendata.ecdc.europa.eu/covid19/casedistribution/csv")
    data.to_csv('data/ECDC/%s.csv' % yesterday)


def collect_data():
    get_data_jhu()
    get_data_ecdc()


schedule.every().day.at("17:02").do(collect_data)
while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
