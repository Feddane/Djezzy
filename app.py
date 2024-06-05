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

@app.route('/reclamation', methods=['GET', 'POST'])
def reclamation():
    if 'username' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        titre = request.form.get('titre')
        sites = request.form.get('sites')
        action_entreprise = request.form.get('action_entreprise')
        date_ouverture = request.form.get('date_ouverture')
        date_fin = request.form.get('date-fin')
        operateur = request.form.get('operateur')
        echeance = request.form.get('echeance')
        etages = request.form.get('etages') 
        affecte_a = request.form.get('affecte_a')
        priorite = request.form.get('priorite')
        acces = request.form.get('acces')
        ouvert_par = request.form.get('ouvert_par')
        description = request.form.get('description')
        status = request.form.get('status')
        categorie = request.form.get('categorie')
        famille = request.form.get('famille')
        commentaire = request.form.get('commentaire')
        fichier = request.files.get('fileUpload')

        if fichier:
            fichier_path = os.path.join(upload_dir, fichier.filename)
            fichier.save(fichier_path)
        else:
            fichier_path = None

        cursor = mysql.connection.cursor()

        cursor.execute('SELECT COUNT(*) FROM reclamation')
        result = cursor.fetchone()
        if result[0] == 0:
            cursor.execute('ALTER TABLE reclamation AUTO_INCREMENT = 1')

        cursor.execute('''INSERT INTO reclamation (titre, sites, action_entreprise, date_ouverture, date_fin, operateur, echeance, etages, affecte_a, priorite, acces, ouvert_par, description, status, categorie, famille, commentaire, fichier) 
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)''',
                       (titre, sites, action_entreprise, date_ouverture, date_fin, operateur, echeance, etages, affecte_a, priorite, acces, ouvert_par, description, status, categorie, famille, commentaire, fichier_path))
        mysql.connection.commit()
        cursor.close()

        return redirect(url_for('reclamation'))

    return render_template('reclamation.html')

@app.route('/historique', methods=['GET'])
def historique():
    if 'username' not in session:
        return redirect(url_for('login'))

    
    if request.args.get('categorie') or request.args.get('date') or request.args.get('status'):
        categorie = request.args.get('categorie')
        date = request.args.get('date')
        status = request.args.get('status')
        
        cursor = mysql.connection.cursor()
        
        query = "SELECT id, categorie, date_ouverture, status FROM reclamation WHERE 1=1"
        params = []

        if categorie:
            query += " AND categorie LIKE %s"
            params.append(f"%{categorie}%")
        if date:
            query += " AND date_ouverture = %s"
            params.append(date)
        if status:
            query += " AND status LIKE %s"
            params.append(f"%{status}%")
        
        cursor.execute(query, params)
        results = cursor.fetchall()
        cursor.close()

        return render_template('historique.html', results=results)
    else:
        
        return render_template('historique.html', results=None)


@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session:
        return redirect(url_for('login'))

    record_id = request.form.get('recordId')
    new_status = request.form.get('newStatus')

    if record_id and new_status:
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE reclamation SET status = %s WHERE id = %s', (new_status, record_id))
        mysql.connection.commit()
        cursor.close()
        flash('Status mis à jour avec succès', 'success')

    return redirect(url_for('historique'))


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
