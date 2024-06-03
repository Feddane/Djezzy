
/*********table_users --> authentification**********/
CREATE TABLE table_users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(20) NOT NULL,
    password VARCHAR(20) NOT NULL
);

/*********reclamation --> table de reclamation**********/
CREATE TABLE reclamation (
    id INT AUTO_INCREMENT PRIMARY KEY,
    titre VARCHAR(255),
    sites VARCHAR(255),
    action_entreprise VARCHAR(255),
    date_ouverture DATE,
    date_fin DATE,
    operateur VARCHAR(255),
    echeance DATE,
    etages VARCHAR(10),
    affecte_a VARCHAR(255),
    priorite VARCHAR(20),
    acces VARCHAR(10),
    ouvert_par VARCHAR(255),
    description TEXT,
    status VARCHAR(20),
    categorie VARCHAR(50),
    famille VARCHAR(50),
    commentaire TEXT,
    fichier VARCHAR(255)
);
