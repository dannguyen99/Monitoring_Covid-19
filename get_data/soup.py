import requests
from bs4 import BeautifulSoup
req = requests.get('https://vi.wikipedia.org/wiki/%C4%90%E1%BA%A1i_d%E1%BB%8Bch_COVID-19_t%E1%BA%A1i_Vi%E1%BB%87t_Nam')
soup = BeautifulSoup(req.text, "lxml")
# data = soup.findAll("li", { "role":"button" })
# names = [d.text for d in data]
# print(names)
print(soup.get_text)