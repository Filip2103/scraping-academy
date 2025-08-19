import requests
from bs4 import BeautifulSoup
import pymysql


conn = pymysql.connect(
    host="localhost",
    user="root",
    password="",
    database="scraping_academy",
    charset="utf8mb4"
)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS cene_kurseva (
    id INT AUTO_INCREMENT PRIMARY KEY,
    program VARCHAR(100),
    akcijska_cena VARCHAR(20),
    puna_cena VARCHAR(20),
    rata_12 VARCHAR(20),
    rata_14 VARCHAR(20)
)
""")

url = "https://www.it-akademija.com/upis-it-akademija-prijavite-se-na-vreme"
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")


tabele = soup.find_all("table", class_="tabela")
tabela = tabele[1]
rows = tabela.find_all("tr")[1:]


for row in rows:
    cols = row.find_all("td")
    program = cols[0].get_text(strip=True)
    akcijska_cena = cols[1].get_text(strip=True)
    puna_cena = cols[2].get_text(strip=True)
    rata_12 = cols[3].get_text(strip=True)
    rata_14 = cols[4].get_text(strip=True)

    print(program, akcijska_cena, puna_cena, rata_12, rata_14)


    cursor.execute("""
        INSERT INTO cene_kurseva (program, akcijska_cena, puna_cena, rata_12, rata_14)
        VALUES (%s, %s, %s, %s, %s)
    """, (program, akcijska_cena, puna_cena, rata_12, rata_14))


conn.commit()
conn.close()

print("Cene uspešno snimljene u MySQL bazu.")
