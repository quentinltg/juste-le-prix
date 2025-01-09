import sqlite3
import requests

# Fonction pour créer la table
def creer_table():

    # Connexion à la base de données
    con = sqlite3.connect("DB/database.db")
    cur = con.cursor()

    # Suppression de la table si elle existe
    cur.execute("DROP TABLE IF EXISTS PRODUIT")

    # Création de la table
    cur.execute("""CREATE TABLE IF NOT EXISTS PRODUIT (
        code VARCHAR(10) PRIMARY KEY,
        nom VARCHAR(255) NOT NULL,
        image VARCHAR(255) NOT NULL,
        prix FLOAT(2) NOT NULL,
        theme VARCHAR(255)
    );""")

    # Commit la création de la table
    con.commit()

    # Ferme la connexion
    con.close()



# Fonction pour insérer un nouveau produit
def inserer_produit(code, theme):

    # Connexion à la base de données
    con = sqlite3.connect("DB/database.db")
    cur = con.cursor()

    # Récupérer les données du produit depuis l'API
    url = "http://ws.chez-wam.info/" + code
    response = requests.get(url)
    if response.status_code == 200:
        json = response.json()
        nom = json.get("title")
        prix = json.get("price").replace("€", "").replace(",", ".")
        image = json.get("images")[0]

        print(f"Récupération des données pour le code produit {code}: title={nom}, price={prix}, image={image}, theme={theme}")

        cur.execute("INSERT OR IGNORE INTO PRODUIT (code, nom, image, prix, theme) VALUES (?, ?, ?, ?, ?)", (code, nom, image, prix, theme))
        con.commit()
    else:
        print(f"Échec de la récupération des données pour le code produit: {code}")

    # Fermer la connexion
    con.close()



# Fonction pour remplir la base de données avec des produits pré-enregistrés
def remplir_produits():
    inserer_produit("B07YQFZ6CJ", "")
    inserer_produit("B0C8J2Y93P", "")
    inserer_produit("B08F5834R7", "")
    # inserer_produit("B08W9JJB76", "Textile") # plus de prix
    inserer_produit("B08T1QXLVJ", "Textile")
    inserer_produit("B08J7QKPL8", "Textile")
    inserer_produit("B098RJXBTY", "Multimedia")
    inserer_produit("B0B5PKW138", "Multimedia")



# Fonction pour récupérer tous les thèmes
def get_themes():

    # Connexion à la base de données
    con = sqlite3.connect("DB/database.db")
    cur = con.cursor()

    # Récupérer tous les thèmes
    cur.execute("SELECT DISTINCT theme FROM PRODUIT")
    themes = cur.fetchall()

    # Fermer la connexion
    con.close()

    return themes



# Fonction pour récupérer les données d'un produit aléatoire en fonction du thème
def get_produit(theme):

    # Connexion à la base de données
    con = sqlite3.connect("DB/database.db")
    cur = con.cursor()

    # Récupérer un produit aléatoire en fonction ou non du thème
    if theme:
        cur.execute("SELECT code, nom, image, prix FROM PRODUIT WHERE theme = ? ORDER BY RANDOM() LIMIT 1", (theme,))
    else:
        cur.execute("SELECT code, nom, image, prix FROM PRODUIT ORDER BY RANDOM() LIMIT 1")

    produit = cur.fetchone()

    # Fermer la connexion
    con.close()

    return produit



# Fonction pour récupérer le prix d'un produit en fonction de son code
def get_prix(code):

    # Connexion à la base de données
    conn = sqlite3.connect('DB/database.db')
    cur = conn.cursor()

    # Récupérer le prix du produit
    cur.execute("SELECT prix FROM PRODUIT WHERE code = ?", (code,))
    prix = float(cur.fetchone()[0])

    # Fermer la connexion
    conn.close()

    return prix



# creer_table()
# remplir_produits()