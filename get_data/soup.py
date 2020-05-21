import requests
from bs4 import BeautifulSoup
req = requests.get('https://vi.wikipedia.org/wiki/Rap')
soup = BeautifulSoup(req.text, "lxml")
print(soup.get_text())