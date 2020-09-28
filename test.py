import requests
from bs4 import BeautifulSoup
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
import json
import pandas as pd

req = requests.get('https://ncov.moh.gov.vn/', verify=False)
soup = BeautifulSoup(req.text, "html.parser")

link_list = soup.findAll('a', {'class':"text-muted"})
patients = []
for link in link_list:
    onclick = link.get('onclick')
    case = onclick[16:-2]
    json_response = requests.get('https://ncov.moh.gov.vn/vi/web/guest/trang-chu?p_p_id=corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v&p_p_lifecycle=2&p_p_state=normal&p_p_mode=view&p_p_resource_id=getThongTinDichTe&p_p_cacheability=cacheLevelPage&_corona_trangchu_top_CoronaTrangchuTopPortlet_INSTANCE_RrVAbIFIPL7v_strValue=' + case, verify=False).text
    json_object = json.loads(json_response)
    patients.append(json_object)

df = pd.json_normalize(patients)
df.to_csv('test_data_scrapping.csv')