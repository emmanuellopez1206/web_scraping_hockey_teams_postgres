from urllib.parse import urlparse
import requests
from bs4 import BeautifulSoup
import psycopg2

connection = psycopg2.connect(
    host = "localhost",
    user = "postgres",
    password = "Vicky120600*",
    database = "test",
    port = "5432"
)
connection.autocommit = True

def crear_tabla():
    cursor = connection.cursor()
    query = "CREATE TABLE hockey_teams(team_name varchar(255),year int8, wins int8, losses int8, ot_losses int8, win_percentage int8, goals_for int8, goals_against int8, mor_less int8)"
    try:
        cursor.execute(query)
    except:
        print("La tabla ya está creada")
    cursor.close()

def obtener_urls():
    urls_all = []
    url = "http://www.scrapethissite.com/pages/forms/"
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    urls = soup.find("ul", attrs={"class":"pagination"}).find_all("li")
    for url in urls:
        u = url.find('a').get("href")
        new_url =f"http://www.scrapethissite.com{u}"
        urls_all.append(new_url)
    return urls_all

def get_data(all):
    ot_losses = all[4].get_text().strip().rstrip()
    ot_losses = ot_losses if ot_losses else 0 
    data = {
        "name" : all[0].get_text().strip().rstrip(),
        "year" : all[1].get_text().strip().rstrip(),
        "wins" : all[2].get_text().strip().rstrip(),
        "losses" : all[3].get_text().strip().rstrip(),
        "ot_losses" : ot_losses,
        "win_percentage" : all[5].get_text().strip().rstrip(),
        "gf" : all[6].get_text().strip().rstrip(),
        "ga" : all[7].get_text().strip().rstrip(),
        "more_less" : all[8].get_text().strip().rstrip()
    }
    return data

def page(rows):
    cursor = connection.cursor()
    for row in rows:
        all = row.find_all('td')
        data = get_data(all)
        query = f""" INSERT INTO hockey_teams (team_name,year, wins, losses, ot_losses, win_percentage, goals_for, goals_against, mor_less) values ('{data["name"]}','{data["year"]}',{data["wins"]},{data["losses"]},{data["ot_losses"]},{data["win_percentage"]},{data["gf"]},{data["ga"]},{data["more_less"]})"""
        cursor.execute(query)
    cursor.close()

def scraping_all_urls(urls_all):
    cursor = connection.cursor()
    for url in urls_all:
        r = requests.get(url) 
        soup = BeautifulSoup(r.content, "html.parser")
        rows = soup.find("table", attrs={"class":"table"}).find_all("tr",attrs={"class":"team"})
        page(rows)
     
if __name__ == "__main__":
    crear_tabla()
    urls = obtener_urls()
    scraping_all_urls(urls)