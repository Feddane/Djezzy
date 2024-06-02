from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

upload_dir = 'static/uploads'
os.makedirs(upload_dir, exist_ok=True)

# Page de connexion
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM table_users WHERE username = %s AND password = %s', (username, password))
        user = cursor.fetchone()
        cursor.close()

        if user:
            session['username'] = username
            return redirect(url_for('reclamation'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')

    return render_template('login.html')


# Page de changement de mot de passe
@app.route('/changer_mdp', methods=['GET', 'POST'])
def changer_mdp():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        username = session.get('username')

        if username:
            cursor = mysql.connection.cursor()
            cursor.execute('SELECT * FROM table_users WHERE username = %s AND password = %s', (username, old_password))
            user = cursor.fetchone()

            if user:
                cursor.execute('UPDATE table_users SET password = %s WHERE username = %s', (new_password, username))
                mysql.connection.commit()
                cursor.close()
                flash('Mot de passe changé avec succès', 'success')
                return redirect(url_for('login'))
            else:
                flash('Ancien mot de passe incorrect', 'error')
        else:
            flash('Vous devez être connecté pour changer de mot de passe', 'error')

    return render_template('changer_mdp.html')

# Page de réclamation
@app.route('/reclamation', methods=['GET', 'POST'])
def reclamation():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titre = request.form['titre']
        sites = request.form['sites']
        action_entreprise = request.form['action_entreprise']
        date_ouverture = request.form['date_ouverture']
        date_fin = request.form['date-fin']
        operateur = request.form['operateur']
        echeance = request.form['echeance']
        etages = request.form['etages']
        affecte_a = request.form['affecte_a']
        priorite = request.form['priorite']
        acces = request.form['acces']
        ouvert_par = request.form['ouvert_par']
        description = request.form['description']
        status = request.form['status']
        categorie = request.form['categorie']
        famille = request.form['famille']
        commentaire = request.form['commentaire']
        fichier = request.files['fileUpload']

        if fichier:
            fichier_path = os.path.join(upload_dir, fichier.filename)
            fichier.save(fichier_path)
        else:
            fichier_path = None

        cursor = mysql.connection.cursor()
        cursor.execute('''INSERT INTO reclamation (titre, sites, action_entreprise, date_ouverture, date_fin, operateur, echeance, etages, affecte_a, priorite, acces, ouvert_par, description, status, categorie, famille, commentaire, fichier) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (titre, sites, action_entreprise, date_ouverture, date_fin, operateur, echeance, etages, affecte_a, priorite, acces, ouvert_par, description, status, categorie, famille, commentaire, fichier_path))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('reclamation'))

    return render_template('reclamation.html')

@app.route('/historique')
def historique():
    return render_template('historique.html')

if __name__ == '__main__':
    app.run(debug=True)
