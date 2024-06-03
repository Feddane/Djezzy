Veuillez suivre ces étapes pour assurer l'exécution du code :

1- Installer Python : Assurez-vous d'installer Python sur votre terminal.

2- Installer Flask : Après l'installation de Python, exécutez la commande suivante dans
votre terminal pour installer Flask et les autres dépendances répertoriées dans le fichier requirements.txt :
            pip install -r requirements.txt

3- Installer WampServer : Installez WampServer pour accéder à PhpMyAdmin (si ce n'est pas déjà fait).
Ensuite, créez une table appelée "users". Copiez tout le code existant dans le fichier table_bdd.sql
et collez-le dans le champ SQL de la table "users" que vous avez créée.

4-Lancer l'application : Enfin, exécutez la commande suivante dans votre terminal :
            python app.py
Puis, accédez à http://127.0.0.1:5000 pour visualiser le site.
