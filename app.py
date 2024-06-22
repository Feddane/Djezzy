from flask import Flask, render_template, request, redirect, url_for, session, flash, send_file, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
import pandas as pd
from io import BytesIO
from graph import bubble, verticalBar, horizentalBar, plotmois
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'

# Configuration pour PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/users'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

upload_dir = 'static/uploads'
os.makedirs(upload_dir, exist_ok=True)

class Admin(db.Model):
    __tablename__ = 'table_admins'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)

class Reclamation(db.Model):
    __tablename__ = 'reclamation'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200))
    sites = db.Column(db.String(200))
    action_entreprise = db.Column(db.String(200))
    date_ouverture = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    operateur = db.Column(db.String(200))
    echeance = db.Column(db.Date)
    etages = db.Column(db.String(200))
    affecte_a = db.Column(db.String(200))
    priorite = db.Column(db.String(200))
    acces = db.Column(db.String(200))
    ouvert_par = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(200))
    categorie = db.Column(db.String(200))
    famille = db.Column(db.String(200))
    commentaire = db.Column(db.Text)
    fichier = db.Column(db.String(200))

class User(db.Model):
    __tablename__ = 'table_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150), nullable=False)
    last_name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class ReclamationUser(db.Model):
    __tablename__ = 'reclamation_users'
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(200))
    sites = db.Column(db.String(200))
    action_entreprise = db.Column(db.String(200))
    date_ouverture = db.Column(db.Date)
    date_fin = db.Column(db.Date)
    operateur = db.Column(db.String(200))
    echeance = db.Column(db.Date)
    etages = db.Column(db.String(200))
    affecte_a = db.Column(db.String(200))
    priorite = db.Column(db.String(200))
    acces = db.Column(db.String(200))
    ouvert_par = db.Column(db.String(200))
    description = db.Column(db.Text)
    status = db.Column(db.String(200))
    categorie = db.Column(db.String(200))
    famille = db.Column(db.String(200))
    commentaire = db.Column(db.Text)
    fichier = db.Column(db.String(200))

class Superviseur(db.Model):
    __tablename__ = 'table_superviseur'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)


@app.route('/')
def home():
    return render_template('dashboard.html')

@app.route('/select_role', methods=['POST'])
def select_role():
    role = request.form.get('role')
    if role == 'admin':
        return redirect(url_for('login_admin'))
    elif role == 'superviseur':
        return redirect(url_for('login_supervisor'))
        pass
    elif role == 'utilisateur':
        return redirect(url_for('login_user'))
    else:
        flash('Rôle non valide', 'error')
        return redirect(url_for('home'))

#all about SUPERVISOR
@app.route('/login_supervisor', methods=['GET', 'POST'])
def login_supervisor():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        supervisor = Superviseur.query.filter_by(username=username, password=password).first()
        if supervisor:
            session['username'] = username
            return redirect(url_for('reclamation_supervisor'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')
    return render_template('supervisor_dashboard.html')

@app.route('/reclamation_supervisor', methods=['GET', 'POST'])
def reclamation_supervisor():
    if 'username' not in session:
        return redirect(url_for('login_supervisor'))

    if request.method == 'POST':
        titre = request.form.get('titre')
        sites = request.form.get('sites')
        action_entreprise = request.form.get('action_entreprise')
        date_ouverture = request.form.get('date_ouverture')
        date_fin = request.form.get('date_fin')
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

        fichier_nom = None

        if fichier:
            fichier_nom = fichier.filename

        nouvelle_reclamation = Reclamation(
            titre=titre,
            sites=sites,
            action_entreprise=action_entreprise,
            date_ouverture=date_ouverture,
            date_fin=date_fin,
            operateur=operateur,
            echeance=echeance,
            etages=etages,
            affecte_a=affecte_a,
            priorite=priorite,
            acces=acces,
            ouvert_par=ouvert_par,
            description=description,
            status=status,
            categorie=categorie,
            famille=famille,
            commentaire=commentaire,
            fichier=fichier_nom
        )

        db.session.add(nouvelle_reclamation)
        db.session.commit()

        return redirect(url_for('reclamation_supervisor'))

    return render_template('reclamation_supervisor.html')

@app.route('/historique_supervisor', methods=['GET'])
def historique_supervisor():
    if 'username' not in session:
        return redirect(url_for('login_supervisor'))

    categorie = request.args.get('categorie')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    status = request.args.get('status')

    query = Reclamation.query

    if categorie:
        query = query.filter(Reclamation.categorie.ilike(f"%{categorie}%"))
    if date_debut and date_fin:
        query = query.filter(Reclamation.date_ouverture.between(date_debut, date_fin))
    if status:
        query = query.filter(Reclamation.status.ilike(f"%{status}%"))


    query = query.order_by(Reclamation.id)

    results = query.all()

    return render_template('historique_supervisor.html', results=results)

def generate_statistic_images(db, mois=None):
    mois_num = None
    if mois:
        mois_num = month_name_to_number(mois)
        if mois_num is None:
            return None, "Invalid month name"

    img_categorie = verticalBar(db, month=mois_num)
    img_famille = bubble(db, month=mois_num)
    img_employe = horizentalBar(db, month=mois_num)
    img_priorite = bubble(db, property="priorite", month=mois_num)
    img_mois = plotmois(db)

    return {
        'img_categorie': img_categorie,
        'img_famille': img_famille,
        'img_employe': img_employe,
        'img_priorite': img_priorite,
        'img_mois': img_mois
    }, None

@app.route('/statistique/data', methods=['GET'])
def statistique_data():
    if 'username' not in session:
        return redirect(url_for('login_supervisor'))

    mois = request.args.get('mois')

    images, error = generate_statistic_images(db, mois)
    if error:
        return error, 400

    return jsonify(images)

@app.route('/statistique', methods=['GET'])
def statistique():
    if 'username' not in session:
        return redirect(url_for('login_supervisor'))

    mois = request.args.get('mois')

    operateur_file_path = os.path.join(app.static_folder, 'operateur.txt')
    try:
        with open(operateur_file_path, 'r', encoding='utf-8') as file:
            operateur_list = file.read().strip().split('\n')
    except FileNotFoundError:
        operateur_list = []

    actifs_count = len(set(operateur_list))

    images, error = generate_statistic_images(db, mois)
    if error:
        return error, 400

    incidents_count = ReclamationUser.query.count()
    categories_count = 10
    reclamations = ReclamationUser.query.order_by(ReclamationUser.id).all()

    return render_template('statistique.html', actifs_count=actifs_count, incidents_count=incidents_count,
                           categories_count=categories_count, reclamations=reclamations, **images)


def month_name_to_number(month_name):
    month_names = {
        'janvier': 1, 'février': 2, 'mars': 3, 'avril': 4,
        'mai': 5, 'juin': 6, 'juillet': 7, 'août': 8,
        'septembre': 9, 'octobre': 10, 'novembre': 11, 'décembre': 12
    }
    return month_names.get(month_name.lower())





#all about USER
@app.route('/login_user', methods=['GET', 'POST'])
def login_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']

        user = User.query.filter_by(username=username, first_name=first_name, last_name=last_name, email=email, password=password).first()

        if user:

            session['username'] = user.first_name
            return redirect(url_for('reclamation_user'))
        else:
            flash('Coordonnées Incorrectes!', 'danger')

    return render_template('user_dashboard.html')


@app.route('/reclamation_user', methods=['GET', 'POST'])
def reclamation_user():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    if request.method == 'POST':
        titre = request.form.get('titre')
        sites = request.form.get('sites')
        action_entreprise = request.form.get('action_entreprise')
        date_ouverture = request.form.get('date_ouverture')
        date_fin = request.form.get('date_fin')
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

        fichier_nom = None

        if fichier:
            fichier_nom = fichier.filename

        nouvelle_reclamation = ReclamationUser(
            titre=titre,
            sites=sites,
            action_entreprise=action_entreprise,
            date_ouverture=date_ouverture,
            date_fin=date_fin,
            operateur=operateur,
            echeance=echeance,
            etages=etages,
            affecte_a=affecte_a,
            priorite=priorite,
            acces=acces,
            ouvert_par=ouvert_par,
            description=description,
            status=status,
            categorie=categorie,
            famille=famille,
            commentaire=commentaire,
            fichier=fichier_nom
        )

        db.session.add(nouvelle_reclamation)
        db.session.commit()

        return redirect(url_for('reclamation_user'))

    return render_template('reclamation_user.html')


@app.route('/historique_user', methods=['GET'])
def historique_user():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    categorie = request.args.get('categorie')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    status = request.args.get('status')

    query = ReclamationUser.query

    if categorie:
        query = query.filter(ReclamationUser.categorie.ilike(f"%{categorie}%"))
    if date_debut and date_fin:
        query = query.filter(ReclamationUser.date_ouverture.between(date_debut, date_fin))
    if status:
        query = query.filter(ReclamationUser.status.ilike(f"%{status}%"))


    query = query.order_by(ReclamationUser.id)

    results = query.all()

    return render_template('historique_user.html', results=results)

@app.route('/all_reclamations_user', methods=['GET'])
def all_reclamations_user():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    reclamations = ReclamationUser.query.order_by(ReclamationUser.id).all()
    results = [{
        'id': r.id,
        'titre': r.titre,
        'sites': r.sites,
        'action_entreprise': r.action_entreprise,
        'date_ouverture': r.date_ouverture.strftime('%Y-%m-%d'),
        'date_fin': r.date_fin.strftime('%Y-%m-%d'),
        'operateur': r.operateur,
        'echeance': r.echeance.strftime('%Y-%m-%d'),
        'etages': r.etages,
        'affecte_a': r.affecte_a,
        'priorite': r.priorite,
        'acces': r.acces,
        'ouvert_par': r.ouvert_par,
        'description': r.description,
        'status': r.status,
        'categorie': r.categorie,
        'famille': r.famille,
        'commentaire': r.commentaire,
        'fichier': r.fichier
    } for r in reclamations]
    return jsonify(results)



@app.route('/export_user', methods=['GET'])
def export_user():
    if 'username' not in session:
        return redirect(url_for('login_user'))

    categorie = request.args.get('categorie')
    date = request.args.get('date')
    status = request.args.get('status')

    query = ReclamationUser.query

    if categorie:
        query = query.filter(ReclamationUser.categorie.like(f"%{categorie}%"))
    if date:
        query = query.filter(ReclamationUser.date_ouverture == date)
    if status:
        query = query.filter(ReclamationUser.status.like(f"%{status}%"))

    results = query.all()

    if not results:
        flash("Le tableau est vide, vous ne pouvez pas exporter de données.", "error")
        return redirect(url_for('historique_user', categorie=categorie, date=date, status=status))

    else:
        columns = ['ID', 'Titre', 'Sites', 'Action Entreprise', 'Date Ouverture', 'Date Fin', 'Opérateur', 'Échéance', 
                   'Étages', 'Affecté À', 'Priorité', 'Accès', 'Ouvert Par', 'Description', 'Status', 'Catégorie', 
                   'Famille', 'Commentaire', 'Fichier']
        df = pd.DataFrame([(r.id, r.titre, r.sites, r.action_entreprise, r.date_ouverture, r.date_fin, r.operateur, r.echeance, 
                            r.etages, r.affecte_a, r.priorite, r.acces, r.ouvert_par, r.description, r.status, r.categorie, 
                            r.famille, r.commentaire, r.fichier) for r in results], columns=columns)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reclamations')
            worksheet = writer.sheets['Reclamations']
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = adjusted_width
        output.seek(0)
        return send_file(output, download_name='reclamations.xlsx', as_attachment=True)




#all about ADMIN
@app.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = Admin.query.filter_by(username=username, password=password).first()

        if user:
            session['username'] = username
            return redirect(url_for('reclamation'))
        else:
            flash('Nom d\'utilisateur ou mot de passe incorrect', 'error')

    return render_template('admin_dashboard.html')

@app.route('/changer_mdp', methods=['GET', 'POST'])
def changer_mdp():
    if request.method == 'POST':
        old_password = request.form['old_password']
        new_password = request.form['new_password']
        username = session.get('username')

        if username:
            user = Admin.query.filter_by(username=username, password=old_password).first()

            if user:
                user.password = new_password
                db.session.commit()
                flash('Mot de passe changé avec succès', 'success')
                return redirect(url_for('login_admin'))
            else:
                flash('Ancien mot de passe incorrect', 'error')
        else:
            flash('Vous devez être connecté pour changer de mot de passe', 'error')

    return render_template('changer_mdp.html')

@app.route('/reclamation', methods=['GET', 'POST'])
def reclamation():
    if 'username' not in session:
        return redirect(url_for('login_admin'))

    if request.method == 'POST':
        titre = request.form.get('titre')
        sites = request.form.get('sites')
        action_entreprise = request.form.get('action_entreprise')
        date_ouverture = request.form.get('date_ouverture')
        date_fin = request.form.get('date_fin')
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

        fichier_nom = None

        if fichier:
            fichier_nom = fichier.filename

        nouvelle_reclamation = Reclamation(
            titre=titre,
            sites=sites,
            action_entreprise=action_entreprise,
            date_ouverture=date_ouverture,
            date_fin=date_fin,
            operateur=operateur,
            echeance=echeance,
            etages=etages,
            affecte_a=affecte_a,
            priorite=priorite,
            acces=acces,
            ouvert_par=ouvert_par,
            description=description,
            status=status,
            categorie=categorie,
            famille=famille,
            commentaire=commentaire,
            fichier=fichier_nom
        )

        db.session.add(nouvelle_reclamation)
        db.session.commit()

        return redirect(url_for('reclamation'))

    return render_template('reclamation.html')

@app.route('/historique', methods=['GET'])
def historique():
    if 'username' not in session:
        return redirect(url_for('login_admin'))

    categorie = request.args.get('categorie')
    date_debut = request.args.get('date_debut')
    date_fin = request.args.get('date_fin')
    status = request.args.get('status')

    query = Reclamation.query

    if categorie:
        query = query.filter(Reclamation.categorie.ilike(f"%{categorie}%"))
    if date_debut and date_fin:
        query = query.filter(Reclamation.date_ouverture.between(date_debut, date_fin))
    if status:
        query = query.filter(Reclamation.status.ilike(f"%{status}%"))

    query = query.order_by(Reclamation.id)

    results = query.all()

    return render_template('historique.html', results=results)


@app.route('/update_status', methods=['POST'])
def update_status():
    if 'username' not in session:
        return redirect(url_for('login'))

    record_id = request.form.get('recordId')
    new_status = request.form.get('newStatus')
    current_status = request.form.get('currentStatus')

    if record_id and new_status and current_status:
        current_status_lower = current_status.lower()
        new_status_lower = new_status.lower()
        if not (current_status_lower == 'inactif' and new_status_lower == 'actif'):

            if 'historique_user' in request.referrer:
                reclamation = ReclamationUser.query.get(record_id)
            else:
                reclamation = Reclamation.query.get(record_id)
            reclamation.status = new_status
            db.session.commit()
            flash('Statut mis à jour avec succès', 'success')
        else:
            flash('Impossible de changer le statut de Inactif à Actif.', 'error')


    if 'historique_user' in request.referrer:
        return redirect(url_for('historique_user'))
    else:
        return redirect(url_for('historique'))

@app.route('/update_date_fin', methods=['POST'])
def update_date_fin():
    if 'username' not in session:
        return redirect(url_for('login'))

    record_id = request.form.get('recordId')
    new_date_fin = request.form.get('newDateFin')

    if record_id and new_date_fin:

        if 'historique_user' in request.referrer:
            reclamation = ReclamationUser.query.get(record_id)
        else:
            reclamation = Reclamation.query.get(record_id)
        reclamation.date_fin = new_date_fin
        db.session.commit()
        flash('Date de fin mise à jour avec succès', 'success')


    if 'historique_user' in request.referrer:
        return redirect(url_for('historique_user'))
    else:
        return redirect(url_for('historique'))


@app.route('/export', methods=['GET'])
def export():
    if 'username' not in session:
        return redirect(url_for('login_admin'))

    categorie = request.args.get('categorie')
    date = request.args.get('date')
    status = request.args.get('status')

    query = Reclamation.query

    if categorie:
        query = query.filter(Reclamation.categorie.like(f"%{categorie}%"))
    if date:
        query = query.filter(Reclamation.date_ouverture == date)
    if status:
        query = query.filter(Reclamation.status.like(f"%{status}%"))

    results = query.all()

    if not results:
        flash("Le tableau est vide, vous ne pouvez pas exporter de données.", "error")
        return redirect(url_for('historique', categorie=categorie, date=date, status=status))

    else:
        columns = ['ID', 'Titre', 'Sites', 'Action Entreprise', 'Date Ouverture', 'Date Fin', 'Opérateur', 'Échéance', 
                   'Étages', 'Affecté À', 'Priorité', 'Accès', 'Ouvert Par', 'Description', 'Status', 'Catégorie', 
                   'Famille', 'Commentaire', 'Fichier']
        df = pd.DataFrame([(r.id, r.titre, r.sites, r.action_entreprise, r.date_ouverture, r.date_fin, r.operateur, r.echeance, 
                            r.etages, r.affecte_a, r.priorite, r.acces, r.ouvert_par, r.description, r.status, r.categorie, 
                            r.famille, r.commentaire, r.fichier) for r in results], columns=columns)
        output = BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Reclamations')
            worksheet = writer.sheets['Reclamations']
            for col in worksheet.columns:
                max_length = 0
                column = col[0].column_letter
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(str(cell.value))
                    except:
                        pass
                adjusted_width = (max_length + 2)
                worksheet.column_dimensions[column].width = adjusted_width
        output.seek(0)
        return send_file(output, download_name='reclamations.xlsx', as_attachment=True)

@app.route('/all_reclamations', methods=['GET'])
def all_reclamations():
    if 'username' not in session:
        return jsonify({'error': 'Unauthorized'}), 401

    reclamations = Reclamation.query.order_by(Reclamation.id).all()
    results = [{
        'id': r.id,
        'titre': r.titre,
        'sites': r.sites,
        'action_entreprise': r.action_entreprise,
        'date_ouverture': r.date_ouverture.strftime('%Y-%m-%d'),
        'date_fin': r.date_fin.strftime('%Y-%m-%d'),
        'operateur': r.operateur,
        'echeance': r.echeance.strftime('%Y-%m-%d'),
        'etages': r.etages,
        'affecte_a': r.affecte_a,
        'priorite': r.priorite,
        'acces': r.acces,
        'ouvert_par': r.ouvert_par,
        'description': r.description,
        'status': r.status,
        'categorie': r.categorie,
        'famille': r.famille,
        'commentaire': r.commentaire,
        'fichier': r.fichier
    } for r in reclamations]
    return jsonify(results)


@app.route('/creer_user', methods=['GET', 'POST'])
def creer_user():
    if request.method == 'POST':
        username = request.form['username']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']


        new_user = User(username=username, first_name=first_name, last_name=last_name, email=email, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Utilisateur créé avec succès!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erreur! Veuillez réessayer.', 'danger')

        return redirect(url_for('creer_user'))

    return render_template('creer_user.html')


@app.route('/creer_superviseur', methods=['GET', 'POST'])
def creer_superviseur():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        new_user = Superviseur(username=username, password=password)

        try:
            db.session.add(new_user)
            db.session.commit()
            flash('Superviseur créé avec succès!', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Erreur lors de la création de superviseur. Veuillez réessayer.', 'danger')

        return redirect(url_for('creer_superviseur'))

    return render_template('creer_superviseur.html')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
