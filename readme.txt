Veuillez suivre ces étapes pour assurer l'exécution du code :

1- Installer Python : Assurez-vous d'installer Python sur votre terminal.

2- Installer Flask : Après l'installation de Python, exécutez la commande suivante dans
votre terminal pour installer Flask et les autres dépendances répertoriées dans le fichier requirements.txt :
            pip install -r requirements.txt

3- Installer postgresql : Installez postgresql (si ce n'est pas déjà fait).
Ensuite, créez DataBase appelée "users".

4- Dans config.py: app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:root@localhost/users'
remplacez : "postgres:root" par votre username et password.

5-Lancer l'application : Enfin, exécutez la commande suivante dans votre terminal :
            python run.py
Puis, accédez à http://127.0.0.1:5000 pour visualiser le site.
