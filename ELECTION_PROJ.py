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
    for p in parametry:
        if "xkraj" in p:
            kraj = p.split("=")[1]
            break

    params = dict(p.split('=') for p in get_url.split('?')[1].split('&'))
    var = params['xvar']    
    obec_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obec_kod}&xvyber={var}"    
    rsp = requests.get(obec_url)
    soup = BeautifulSoup(rsp.content, 'html.parser')


    # data
    volici = soup.find_all("td", headers="sa2")[0].text.replace(u'\xa0', u' ')
    obalky = soup.find_all("td", headers="sa3")[0].text.replace(u'\xa0', u' ')
    hlasy = soup.find_all("td", headers="sa6")[0].text.replace(u'\xa0', u' ')
    # nalezení názvů stran
    strany = []
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')

            if len(cells) > 0:
                strana = cells[1].text.strip()
                if strana !="-" and strana != "1":
                    strany.append(strana)
    # hlasy pro strany
    strana_hlasy = []
    for s in strany:
        strana_hlasy.append(soup.find("td", string=strana).find_next_sibling("td").text.replace(u'\xa0', u' ').strip())
    

  