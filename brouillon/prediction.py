from pickle import load
import pandas as pd
from pathlib import Path

DOSSIER_COURANT = Path(__file__).resolve().parent

def predire_groupe_nouvel_individu(coordonnees_axes):
    """Prend en entrée la liste des coordonnées de l'individu sur les axes de l'ACM

    Ex: [0.457155, 0.367339, -0.174715, -0.304713, -0.125955]
    Et retourne la prédiction finale.
    """
    # Scikit-learn requiert une matrice 2D (un tableau de lignes)
    # On transforme le vecteur en [[coord1, coord2, ...]]
    model_predictif = load(open(DOSSIER_COURANT / "model_predictif.pkl", "rb"))
    X_new = [coordonnees_axes]

    # A. Prédire la classe finale
    classe_predite = model_predictif.predict(X_new)[0]

    # B. Obtenir les probabilités de certitude pour chaque classe
    probabilites = model_predictif.predict_proba(X_new)[0]
    classes_du_modele = model_predictif.classes_

    # Structurer le résultat pour ton application
    details_probabilites = {
        cl: f"{prob * 100:.2f}%" for cl, prob in zip(classes_du_modele, probabilites)
    }

    return {
        "classe_predite": classe_predite,
        "probabilites_detail": details_probabilites,
    }
