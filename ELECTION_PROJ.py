"""
projektJUNEK.py:poslední projekt do Engeto Online Python Akademie
author: Vojtěch Junek
email: vojta.junek@tiscali.cz
discord: jsemnamol#8198
"""
import requests
import sys
import csv
import pandas as pd
from bs4 import BeautifulSoup



# url webu a název cesta_souboruu, který zadáváme při spuštění
get_url = sys.argv[1]
cesta_souboru = sys.argv[2]
rsp = requests.get(get_url)
soup = BeautifulSoup(rsp.content, 'html.parser')

# Hledáme kód a název obce na stránce pomocí 'findAll' z knihovny BeautifulSoup.
# Konkrétně hledá elementy "td" s třídou "cislo".
td = soup.findAll("td", class_="cislo")
print("STAHUJI DATA Z VYBRANÉHO URL: ",get_url)

# Inicializace prázdného seznamu pro data
data_to_write = []

for td_el in td:
    get_url_obce = td_el.find('a')['href']
    obec_kod = get_url_obce.split('&')[2].split('=')[1]
    nazev_obec = td_el.find_next_sibling("td", class_="overflow_name").text.strip()
    # split podle '?' a nasledně split podle '&'
    url_split = get_url.split("?")[1]    
    parametry = url_split.split("&")
    # pro každe p v parametrech se zkontroluje
    # pokud obsahuje "xkraj", když ano, tak rozdělíme kraj pomocí "="  
    for p in parametry:
        if "xkraj" in p:            
            kraj = p.split("=")[1]
            break

    params = dict(p.split('=') for p in get_url.split('?')[1].split('&'))
    numnuts = params['xnumnuts']    
    obec_url = f"https://www.volby.cz/pls/ps2017nss/ps311?xjazyk=CZ&xkraj={kraj}&xobec={obec_kod}&xvyber={numnuts}"    
    rsp = requests.get(obec_url)
    soup = BeautifulSoup(rsp.content, 'html.parser')
    # data volicu
    volici = soup.find_all("td", headers="sa2")[0].text.replace(u'\xa0', u' ')
    # data obalky
    obalky = soup.find_all("td", headers="sa3")[0].text.replace(u'\xa0', u' ')
    # data hlasy
    hlasy = soup.find_all("td", headers="sa6")[0].text.replace(u'\xa0', u' ')
    
    # nalezení názvů stran
    strany = []
    tbl = soup.find_all('table')
    for t in tbl:
        radky = t.find_all('tr')
        for r in radky:
            bunky = r.find_all('td')
            if len(bunky) > 0:
                strana = bunky[1].text.strip()
                if strana != "1" and strana !="-":
                    strany.append(strana)
    # hlasy pro strany
    strana_hlasy = []
    for strana in strany:
        strana_hlasy.append(soup.find("td", string=strana).find_next_sibling("td").text.replace(u'\xa0', u' ').strip())
        
    # Přidání aktuálního řádku dat do seznamu data_to_write
    data_to_write.append([nazev_obec, obec_kod, volici, obalky, hlasy] + strany)



     #data do CSV 
    with open(cesta_souboru, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        if csvfile.tell() == 0:  
            writer.writerow(["OBEC NAZEV", "KÓD OBCE", "VOLICI", "OBALKY", "HLASY"] + strany)
        writer.writerow([nazev_obec, obec_kod, volici, obalky, hlasy] + strana_hlasy)
#print("UKLÁDÁM DO SOUBORU S CESTOU: ",cesta_souboru)        
#print("ukoncuji ELECTION-SCRAPER")
# Seznam názvů sloupců obsahující všechny sloupce z data_to_write a navíc další sloupce

#columns = ["OBEC NAZEV", "KÓD OBCE", "VOLICI", "OBALKY", "HLASY"] + strany
#df = pd.DataFrame(data=data_to_write, columns=columns)

# Zápis do CSV souboru s nastavením kódování na UTF-8
#df.to_csv(cesta_souboru, sep=';', encoding='utf-8', index=False)
#print("Data byla uložena do souboru:", cesta_souboru)







    
    

  