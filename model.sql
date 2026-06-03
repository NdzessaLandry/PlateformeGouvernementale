CREATE TABLE Entreprise(id_entreprise INTEGER PRIMARY KEY AUTOINCREMENT,
                      conctact VARCHAR(255) NOT NULL,
                      description_ VARCHAR(255) NOT NULL,
                      raison_sociale VARCHAR(255) NOT NULL,
                      region INTEGER,
                      statut INTEGER,
                      secteur_activite INTEGER,
                      taille INTEGER,
                      anciennete INTEGER,
                      classe INTEGER,
    FOREIGN KEY (region) REFERENCES Region(id_region),
    FOREIGN KEY (statut) REFERENCES Statut(id_statut),
    FOREIGN KEY (secteur_activite) REFERENCES SecteurActivite(id_secteur_activite),
    FOREIGN KEY (taille) REFERENCES Taille(id_taille),
    FOREIGN KEY (anciennete) REFERENCES Anciennete(id_anciennete),
    FOREIGN KEY (classe) REFERENCES Classe(id_classe)
);
CREATE TABLE Region(id_region INTEGER PRIMARY KEY AUTOINCREMENT,
                    libele VARCHAR(255) NOT NULL
);
CREATE TABLE Statut(id_statut INTEGER PRIMARY KEY AUTOINCREMENT ,
                    libele VARCHAR(255) NOT NULL
);
CREATE TABLE SecteurActivite(id_secteur_activite INTEGER PRIMARY KEY AUTOINCREMENT,
                            libele VARCHAR(255) NOT NULL
);
CREATE TABLE Taille(id_taille INTEGER PRIMARY KEY AUTOINCREMENT,
                   libele VARCHAR(255) NOT NULL
);
CREATE TABLE Anciennete(id_anciennete INTEGER PRIMARY KEY AUTOINCREMENT ,
                      libele VARCHAR(255) NOT NULL
);
CREATE TABLE Classe(id_classe INTEGER PRIMARY KEY AUTOINCREMENT,
                    libele VARCHAR(255) NOT NULL
);
CREATE TABLE ReponseBesoins(
                        id_entreprise INTEGER,
                        id_classe INTEGER,
                        PRIMARY KEY (id_entreprise, id_classe),
                        FOREIGN KEY (id_entreprise) REFERENCES Entreprise(id_entreprise),
                        FOREIGN KEY (id_classe) REFERENCES Classe(id_classe)
);