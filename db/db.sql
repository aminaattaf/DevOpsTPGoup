CREATE TABLE personnes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(100) NOT NULL,
    prenom VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

INSERT INTO personnes(nom, prenom, email) VALUES
('nom1', 'prenom1', 'mail1'),
('nom2', 'prenom2', 'mail2');