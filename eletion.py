from bs4 import BeautifulSoup
import requests


# Send a GET request to the website
url = "https://www.volby.cz/pls/ps2017nss/ps3?xjazyk=CZ"
page = requests.get(url)
print(page)
