import sqlite3
import requests

con = sqlite3.connect("DB/ma_db.db")
cur = con.cursor()

# Création des tables
cur.execute("""CREATE TABLE IF NOT EXISTS PRODUIT (
    produit_code TEXT PRIMARY KEY,
    nom TEXT,
    image TEXT,
    prix REAL
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS PRODUIT_TEXTILE (
    produit_code TEXT PRIMARY KEY
);""")

cur.execute("""CREATE TABLE IF NOT EXISTS PRODUIT_MULTIMEDIA (
    produit_code TEXT PRIMARY KEY
);""")

# Commit the table creation
con.commit()

# Fonction d'insertion de produit
def inserer(str):
    url = "http://ws.chez-wam.info/" + str
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        product_code = str
        nom = json.get("title", "Unknown Product")
        prix = float(json.get("price", "0").replace("€", "").replace(",", ".").strip())
        image = json.get("images", [""])[0]

        # Print the fetched data
        print(f"Fetched data for product code {str}: title={nom}, price={prix}, images={image}")

        sql = "INSERT OR IGNORE INTO PRODUIT (produit_code, nom, image, prix) VALUES (?, ?, ?, ?)"
        val = (product_code, nom, image, prix)
        cur.execute(sql, val)
        con.commit()
    else:
        print(f"Failed to fetch data for product code: {str}")

# Insertion de quelques produits
inserer("B07YQFZ6CJ")
inserer("B0C8J2Y93P")
inserer("B08F5834R7")

# Insertion dans les thèmes PRODUIT_TEXTILE et PRODUIT_MULTIMEDIA
def insert_product(theme, product_code):
    cur.execute(f"INSERT OR IGNORE INTO {theme} (produit_code) VALUES (?)", (product_code,))
    con.commit()

insert_product('PRODUIT_TEXTILE', 'B08W9JJB76')
insert_product('PRODUIT_TEXTILE', 'B08J7QKPL8')
insert_product('PRODUIT_MULTIMEDIA', 'B098RJXBTY')
insert_product('PRODUIT_MULTIMEDIA', 'B0B5PKW138')

# Vérification
res = cur.execute("SELECT * FROM PRODUIT")
print("Produits dans la base :", res.fetchall())

con.close()