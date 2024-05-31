from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'users'

mysql = MySQL(app)

# Page d'enregistrement
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        cursor = mysql.connection.cursor()
        cursor.execute('INSERT INTO table_users (username, password) VALUES (%s, %s)', (username, password))
        mysql.connection.commit()
        cursor.close()

        session['username'] = username
        return redirect(url_for('reclamation'))

    return render_template('login.html')

# Page de réclamation
@app.route('/reclamation')
def reclamation():
    if 'username' in session:
        return render_template('reclamation.html')
    else:
        return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
