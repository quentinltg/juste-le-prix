from flask import Flask, request, render_template, redirect, url_for, session
from DB import ProduitDB, PartieDB

app = Flask(__name__)
app.secret_key = 'ekip_abcq'

@app.route('/', methods=['GET','POST'])
def index():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        return redirect(url_for('jeu_get', pseudo=pseudo))
    return render_template('index.html')



@app.route('/jeu', methods=['GET'])
def jeu_get():

    # Récupérer le pseudo et le thème en paramètres
    pseudo = request.args.get('pseudo')
    theme = request.args.get('theme', '')

    # Initialiser le score du joueur
    session['score'] = 0

    # Récupérer les données du produit
    code_produit, nom_produit, image, prix = ProduitDB.get_produit(theme)

    return render_template('jeu.html', pseudo=pseudo, theme=theme, score=0, image=image, nom=nom_produit, prix=prix, code=code_produit)



@app.route('/jeu', methods=['POST'])
def jeu_post():

    # Récupérer les données
    pseudo = request.form['pseudo']
    theme = request.form.get('theme', '')
    guess = float(request.form['prix'])
    code_produit = request.form['code_produit']
    image = request.form['image']
    nom_produit = request.form['nom']

    # Récupérer le prix du produit
    actual_prix = ProduitDB.get_prix(code_produit)

    # Comparer le prix du produit avec le prix proposé par le joueur
    if guess < actual_prix:
        result = "C'est plus !"
        session['score'] += 1
        correct_guess = False
    elif guess > actual_prix:
        result = "C'est moins !"
        session['score'] += 1
        correct_guess = False
    else:
        result = "Félicitations ! Vous avez trouvé le juste prix ! Essayez de deviner celui du produit suivant..."
        session['score'] += 1
        correct_guess = True

        # Insérer la partie du joueur dans la base de données
        PartieDB.inserer_partie(pseudo, session['score'], code_produit)

    return render_template('jeu.html', pseudo=pseudo, score=session['score'], theme=theme, image=image, nom=nom_produit, code=code_produit, result=result, correct_guess=correct_guess)

if __name__ == '__main__':
    app.run(debug=True)