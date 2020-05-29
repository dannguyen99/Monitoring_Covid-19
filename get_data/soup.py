import requests
import csv
from bs4 import BeautifulSoup
req = requests.get('https://ncov.moh.gov.vn/')
soup = BeautifulSoup(req.text, "lxml")
# table = soup.find("table",{"class":"wikitable sortable mw-collapsible"})
print(soup.get_text())
# output_rows = []
# for table_row in table.findAll('tr'):
#     columns = table_row.findAll('td')
#     output_row = []
#     for column in columns:
#         output_row.append(column.text)
#     output_rows.append(output_row)
#
# with open('output.csv', 'w') as csvfile:
#     writer = csv.writer(csvfile)
#     writer.writerows(output_rows)