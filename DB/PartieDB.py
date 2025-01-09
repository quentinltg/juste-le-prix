import sqlite3

# Fonction pour créer la table
def creer_table():

    # Connexion à la base de données
    con = sqlite3.connect("database.db")
    cur = con.cursor()

    # Suppression de la table si elle existe
    cur.execute("DROP TABLE IF EXISTS PARTIE")

    # Création de la table
    cur.execute("""CREATE TABLE IF NOT EXISTS PARTIE (
        id_partie INTEGER PRIMARY KEY AUTOINCREMENT,
        pseudo VARCHAR(100),
        score INTEGER NOT NULL,
        code_produit VARCHAR(10) NOT NULL,
        FOREIGN KEY(code_produit) REFERENCES PRODUIT(code)
    );""")

    # Commit la création de la table
    con.commit()

    # Fermer la connexion
    con.close()



# Fonction pour insérer une nouvelle partie
def inserer_partie(pseudo, score, code_produit):

    # Connexion à la base de données
    con = sqlite3.connect('DB/database.db')
    cur = con.cursor()

    # Insertion de la partie
    cur.execute("INSERT INTO PARTIE (pseudo, score, code_produit) VALUES (?, ?, ?)", (pseudo, score, code_produit))

    # Commit les changements
    con.commit()

    # Fermer la connexion
    con.close()



# Fonction pour récupérer les logs joueur avec son pseudo
def get_joueurs(pseudo):

    # Connexion à la base de données
    con = sqlite3.connect('DB/database.db')
    cur = con.cursor()

    # Récupération des logs du joueur
    cur.execute("SELECT * FROM PARTIE WHERE pseudo = ?", (pseudo,))
    joueurs = cur.fetchall()

    # Fermer la connexion
    con.close()

    return joueurs



# Supprime un joueur en cas de besoin avec son pseudo et le code du produit
def delete_joueur(pseudo, code_produit):

    # Connexion à la base de données
    con = sqlite3.connect('DB/database.db')
    cur = con.cursor()

    # Suppression du joueur
    cur.execute("DELETE FROM PARTIE WHERE pseudo = ? AND code_produit = ?", (pseudo, code_produit))

    # Commit les changements
    con.commit()

    # Fermer la connexion
    con.close()



# creer_table()