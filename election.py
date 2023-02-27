


# Send a GET request to the website

"""
slama_projekt.py: třetí projekt do Engeto Online Python Akademie
author: David Sláma
email: cimka1@seznam.cz
discord: cimka1#2497
"""
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

    # vytvoření URL pro obec
    url_obec = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obec_kod}&xvyber={numnuts}"

    # získání HTML obsahu stránky s výsledky voleb pro obec
    rsp = requests.get(url_obec)
    soup = BeautifulSoup(rsp.content, 'html.parser')


    # nalezení potřebných dat
    volici_v_seznamu = soup.find_all("td", headers="sa2")[0].text.replace(u'\xa0', u' ')
    vydane_obalky = soup.find_all("td", headers="sa3")[0].text.replace(u'\xa0', u' ')
    platne_hlasy = soup.find_all("td", headers="sa6")[0].text.replace(u'\xa0', u' ')

    # nalezení názvů stran
    strany = []
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cells = row.find_all('td')
            if len(cells) > 0:
                strana = cells[1].text.strip()
                if strana != "1" and strana !="-":
                    strany.append(strana)

    # nalezení platných hlasů pro jednotlivé strany
    platne_hlasy_stran = []
    for strana in strany:
        platne_hlasy_stran.append(soup.find("td", string=strana).find_next_sibling("td").text.replace(u'\xa0', u' ').strip())

    # zápis dat do daného souboru
    with open(cesta_souboru, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')

        if csvfile.tell() == 0:  
            writer.writerow(["Název obce", "Kód obce", "Volici v seznamu", "Vydane obalky", "Platne hlasy"] + strany)
        writer.writerow([nazev_obec, obec_kod, volici_v_seznamu, vydane_obalky, platne_hlasy] + platne_hlasy_stran)