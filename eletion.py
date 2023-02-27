



import requests
import sys
import csv
from bs4 import BeautifulSoup


# url webu a název cesta_souboruu, který zadáváme při spuštění
get_url = sys.argv[1]
cesta_souboru = sys.argv[2]
rsp = requests.get(get_url)
soup = BeautifulSoup(rsp.content, 'html.parser')

# Hledáme kód a název obce na stránce pomocí 'findAll' z knihovny BeautifulSoup.
# Konkrétně hledá elementy "td" s třídou "cislo".
td = soup.findAll("td", class_="cislo")

for td_el in td:
    get_url_obce = td_el.find('a')['href']
    obec_kod = get_url_obce.split('&')[2].split('=')[1]
    nazev_obec = td_el.find_next_sibling("td", class_="overflow_name").text.strip()

    # split podle '?' a nasledně split podle '&'
    url_split = get_url.split("?")[1]    
    parametry = url_split.split("&")
    # hodnoty parametru xkraj
    # split podle '='
    for param in parametry:
        if "xkraj" in param:
            kraj = param.split("=")[1]
            break

    params = dict(param.split('=') for param in get_url.split('?')[1].split('&'))
    numnuts = params['xnumnuts']

   
