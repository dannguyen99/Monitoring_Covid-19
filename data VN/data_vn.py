import requests
import csv
from bs4 import BeautifulSoup

req = requests.get('https://ncov.moh.gov.vn/', verify = False)
soup = BeautifulSoup(req.text, "lxml")
table_ncov = soup.find_all("table", {"class": "table table-striped table-covid19"})
headers_city = "City, Total cases, Active, Recovered, Death"
header_patient = "Patient number, Age, Gender, Location, Status, Nationality"

def get_data_vn(table):
    output_rows = []
    for table_row in table.findAll('tr'):
        columns = table_row.findAll('td')
        output_row = []
        for column in columns:
            output_row.append(column.text)
        output_rows.append(output_row)
    return output_rows
def makefile(file, output_rows, headers):
    with open(file, 'w') as csvfile:
        csvfile.write(headers)
        writer = csv.writer(csvfile)
        writer.writerows(output_rows)

city = makefile('output_ct.csv',get_data_vn(table_ncov[0]),headers_city)
patient = makefile('output_pt.csv',get_data_vn(table_ncov[1]),header_patient)
