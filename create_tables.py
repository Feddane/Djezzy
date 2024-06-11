from app import app, db, Admin


app.app_context().push()

# Créez toutes les tables dans la base de données
db.create_all()

# Ajout des enregistrements dans la table Admin
admins_data = [
    {'username': 'badressine.kihal', 'password': '1234'},
    {'username': 'bilal.sadaoui', 'password': '1234'},
    {'username': 'farid.ferhouh', 'password': '1234'},
    {'username': 'farouk.mammeri', 'password': '1234'},
    {'username': 'fouad.fakir', 'password': '1234'},
    {'username': 'karim.arribi', 'password': '1234'},
    {'username': 'abdelam.remram', 'password': '1234'},
    {'username': 'fouzi.guemar', 'password': 'NS.2023++'},
    {'username': 'lotfi.hadjsaid', 'password': '1234'},
    {'username': 'mostefa.reguieg', 'password': '20051988'}
]

for admin_data in admins_data:
    admin = Admin(**admin_data)
    db.session.add(admin)

db.session.commit()
