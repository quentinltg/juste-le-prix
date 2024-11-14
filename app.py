from flask import Flask, request, render_template, redirect, url_for
import sqlite3

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/jeu', methods=['GET'])
def jeu():
    pseudo = request.args.get('pseudo')
    theme = request.args.get('theme', 'PRODUIT')
    if not pseudo:
        return redirect(url_for('index'))

    conn = sqlite3.connect('DB/ma_db.db')
    c = conn.cursor()
    try:
        # Jointure pour récupérer les détails des produits même pour PRODUIT_TEXTILE et PRODUIT_MULTIMEDIA
        c.execute(f"""
            SELECT p.produit_code, p.nom, p.image, p.prix 
            FROM {theme} t
            JOIN PRODUIT p ON t.produit_code = p.produit_code
            ORDER BY RANDOM() LIMIT 1
        """)
        product_data = c.fetchone()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return render_template('jeu.html', pseudo=pseudo, theme=theme, error="Erreur de base de données.")
    finally:
        conn.close()

    if product_data:
        product_code, nom, image, prix = product_data
        return render_template('jeu.html', pseudo=pseudo, image=image, nom=nom, prix=prix, theme=theme)
    else:
        return render_template('jeu.html', pseudo=pseudo, theme=theme, error="Aucun produit trouvé pour le thème sélectionné.")

if __name__ == '__main__':
    app.run(debug=True)
