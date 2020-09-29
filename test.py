import pandas as pd
import json
import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

df = pd.read_csv('test_data_scrapping.csv')

req = requests.get('https://ncov.moh.gov.vn/', verify=False)
soup = BeautifulSoup(req.text, "html.parser")

table_rows = soup.find_all('tr')
# for row in table_rows[1:]:
#     print(row.find_all('td')[-1].text)

nationality_serie = pd.Series(row.find_all('td')[-1].text for row in table_rows[1:])
df = df.assign(nationality=nationality_serie)
print(df.tail())