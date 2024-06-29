from . import db


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
    role = db.Column(db.String(50), nullable=False)
    def __repr__(self):
        return f'<Reclamation {self.id} - {self.role}>'

class User(db.Model):
    __tablename__ = 'table_users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)


class Superviseur(db.Model):
    __tablename__ = 'table_superviseur'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String(150), nullable=False)