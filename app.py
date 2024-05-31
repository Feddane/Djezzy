from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

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
@app.route('/reclamation')
def reclamation():
    if 'username' in session:
        return render_template('reclamation.html')
    else:
        return redirect(url_for('login'))

@app.route('/historique')
def historique():
    return render_template('historique.html')

if __name__ == '__main__':
    app.run(debug=True)
