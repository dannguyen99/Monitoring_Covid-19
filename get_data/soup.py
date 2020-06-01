import requests
import csv
from bs4 import BeautifulSoup

req = requests.get('https://ncov.moh.gov.vn/', verify = False)
soup = BeautifulSoup(req.text, "lxml")

def get_data_vn():
    table_city = soup.find_all("table", {"class": "table table-striped table-covid19"})[0]
    output_rows = []
    for table_row in table_city.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    with open('output.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)