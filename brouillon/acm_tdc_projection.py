"""
ACM - Tableau Disjonctif Complet (TDC) et Projection dans l'espace factoriel
=============================================================================
Ce module permet de :
  1. Définir les modalités de chaque variable
  2. Encoder un individu (ou une ligne de données) en TDC (one-hot)
  3. Charger les résultats ACM (coordonnées des modalités) depuis un fichier
  4. Projeter un nouvel individu dans l'espace factoriel de l'ACM
  5. Calculer les distances entre individus projetés
"""

import numpy as np
import pandas as pd
from pathlib import Path


# ─────────────────────────────────────────────────────────────────────────────
# 1. DÉFINITION DES VARIABLES ET MODALITÉS
# ─────────────────────────────────────────────────────────────────────────────

VARIABLES = {
    "statut_juridique": [
        "SA", "Cooperative", "SARL", "Entreprise Individuelle",
        "SUARL/SARLU", "GIC", "GIE"
    ],
    "region": [
        "Littoral", "Sud-Ouest", "Nord", "Centre", "Adamaoua",
        "Sud", "Extreme-Nord", "Ouest", "Est", "Nord-Ouest"
    ],
    "taille_entreprise": [
        "Grande Entreprise", "Moyenne Entreprise",
        "Petite Entreprise", "Tres Petite Entreprise"
    ],
    "date_debut_activite": [
        "20 ans et plus", "10 a 19 ans", "5 a 9 ans",
        "3 a 4 ans", "Moins de 3 ans", "Non renseigne"
    ],
    "secteur_activite_princ": [
        "Technologies de l'information et de la communication (TIC)",
        "Agriculture et Agroalimentaire",
        "Industrie manufacturiere",
        "Services professionnels (consulting, comptabilite, etc.)",
        "Secteur minier et extraction",
        "Construction et genie civil",
        "Medias et divertissement",
        "Education et formation",
        "Sante et services medicaux",
        "Tourisme et hotellerie",
        "Commerce de detail et de gros",
        "Energie et services publics",
        "Art, culture locale, etc.",
        "Transport et logistique",
        "Services immobiliers",
        "Services financiers et bancaires"
    ],
    "besoin_intrants":            ["Oui", "Non"],
    "besoin_financement":         ["Oui", "Non"],
    "besoin_emballages":          ["Oui", "Non"],
    "besoin_transport":           ["Oui", "Non"],
    "besoin_appui_entreprise":    ["Oui", "Non"],
    "besoin_equipements":         ["Oui", "Non"],
    "besoin_innovation_recherche":["Oui", "Non"],
}

# Nombre total de colonnes dans le TDC
TOTAL_MODALITES = sum(len(v) for v in VARIABLES.values())


# ─────────────────────────────────────────────────────────────────────────────
# 2. CONSTRUCTION DU TABLEAU DISJONCTIF COMPLET (TDC) — 1 INDIVIDU
# ─────────────────────────────────────────────────────────────────────────────

def construire_tdc_individu(reponses: dict) -> pd.Series:
    """
    Construit la ligne TDC (vecteur binaire 0/1) pour un individu.

    Parameters
    ----------
    reponses : dict
        Dictionnaire {nom_variable: modalite_choisie}.
        Exemple :
            {
                "statut_juridique": "SARL",
                "region": "Littoral",
                "taille_entreprise": "Petite Entreprise",
                "date_debut_activite": "5 a 9 ans",
                "secteur_activite_princ": "Agriculture et Agroalimentaire",
                "besoin_intrants": "Oui",
                "besoin_financement": "Non",
                "besoin_emballages": "Oui",
                "besoin_transport": "Non",
                "besoin_appui_entreprise": "Oui",
                "besoin_equipements": "Non",
                "besoin_innovation_recherche": "Oui",
            }

    Returns
    -------
    pd.Series : vecteur TDC indexé par les noms de colonnes "variable_modalite"
    """
    colonnes = []
    valeurs  = []

    for var, modalites in VARIABLES.items():
        modalite_choisie = reponses.get(var)
        if modalite_choisie is None:
            raise ValueError(f"Variable manquante dans les réponses : '{var}'")
        if modalite_choisie not in modalites:
            raise ValueError(
                f"Modalité '{modalite_choisie}' inconnue pour '{var}'.\n"
                f"Modalités valides : {modalites}"
            )
        for m in modalites:
            colonnes.append(f"{var}_{m}")
            valeurs.append(1 if m == modalite_choisie else 0)

    s=pd.Series(valeurs, index=colonnes, dtype=int)
    dictio={f'{col}':[s.loc[col]] for col in colonnes}

    #df_final = s.reindex(list(VARIABLES.keys()), fill_value=0).to_frame().T

    return pd.DataFrame(dictio)


#──────────────────────────────────────────────────────────────────
# 3. CHARGEMENT DES RÉSULTATS ACM (coordonnées des modalités)
# ─────────────────────────────────────────────────────────────────────────────

def charger_coordonnees_modalites(chemin_fichier: str) -> pd.DataFrame:
    """
    Charge les coordonnées factorielles des modalités issues de l'ACM.

    Format attendu (CSV ou Excel) :
        - Colonne "modalite" : nom de la modalité au format "variable__modalite"
        - Colonnes "Dim1", "Dim2", ... : coordonnées sur chaque axe factoriel

    Parameters
    ----------
    chemin_fichier : str
        Chemin vers le fichier CSV ou Excel contenant les coordonnées.

    Returns
    -------
    pd.DataFrame indexé par le nom des modalités.
    """
    path = Path(chemin_fichier)
    if path.suffix in (".xlsx", ".xls"):
        df = pd.read_excel(chemin_fichier)
    else:
        df = pd.read_csv(chemin_fichier)

    if "modalite" not in df.columns:
        raise ValueError("Le fichier doit contenir une colonne 'modalite'.")

    df = df.set_index("modalite")
    return df


# ─────────────────────────────────────────────────────────────────────────────
# 4. PROJECTION D'UN NOUVEL INDIVIDU DANS L'ESPACE FACTORIEL
# ─────────────────────────────────────────────────────────────────────────────

def projeter_individu(
    tdc_ligne: pd.Series,
    coord_modalites: pd.DataFrame
) -> pd.Series:
    """
    Projette un individu dans l'espace factoriel de l'ACM.

    La coordonnée de l'individu sur chaque axe est la moyenne des coordonnées
    des modalités qu'il a choisies (formule barycentrique ACM).

    Parameters
    ----------
    tdc_ligne : pd.Series
        Ligne TDC de l'individu (vecteur binaire).
    coord_modalites : pd.DataFrame
        Coordonnées factorielles des modalités (index = noms de modalités).

    Returns
    -------
    pd.Series : coordonnées de l'individu sur chaque axe factoriel.
    """
    # Modalités actives (valeur == 1) présentes dans le tableau de coordonnées
    modalites_actives = [
        col for col, val in tdc_ligne.items()
        if val == 1 and col in coord_modalites.index
    ]

    if not modalites_actives:
        raise ValueError("Aucune modalité active trouvée dans les coordonnées ACM.")

    coords = coord_modalites.loc[modalites_actives]
    return coords.mean(axis=0)


def projeter_dataframe(
    tdc: pd.DataFrame,
    coord_modalites: pd.DataFrame
) -> pd.DataFrame:
    """
    Projette tous les individus d'un TDC dans l'espace factoriel.

    Returns
    -------
    pd.DataFrame : coordonnées factorielles (n_individus × n_axes)
    """
    projections = [
        projeter_individu(tdc.iloc[i], coord_modalites)
        for i in range(len(tdc))
    ]
    return pd.DataFrame(projections).reset_index(drop=True)


# ─────────────────────────────────────────────────────────────────────────────
# 5. CALCULS COMPLÉMENTAIRES
# ─────────────────────────────────────────────────────────────────────────────

def distance_euclidienne(coord1: pd.Series, coord2: pd.Series) -> float:
    """Distance euclidienne entre deux individus projetés."""
    return float(np.sqrt(((coord1 - coord2) ** 2).sum()))


def individus_les_plus_proches(
    individu_cible: pd.Series,
    projections: pd.DataFrame,
    n: int = 5
) -> pd.DataFrame:
    """
    Retourne les n individus les plus proches de l'individu cible.

    Parameters
    ----------
    individu_cible : pd.Series  — coordonnées de l'individu à comparer
    projections    : pd.DataFrame — coordonnées de tous les individus
    n              : int — nombre de voisins à retourner

    Returns
    -------
    pd.DataFrame avec colonnes ['index_individu', 'distance']
    """
    distances = projections.apply(
        lambda row: distance_euclidienne(individu_cible, row), axis=1
    )
    distances_sorted = distances.sort_values().head(n)
    return pd.DataFrame({
        "index_individu": distances_sorted.index,
        "distance": distances_sorted.values
    })


def contribution_modalites(tdc_ligne: pd.Series) -> pd.DataFrame:
    """
    Résumé des modalités choisies par un individu.

    Returns
    -------
    pd.DataFrame avec colonnes ['variable', 'modalite']
    """
    rows = []
    for col, val in tdc_ligne.items():
        if val == 1:
            var, mod = col.split("__", 1)
            rows.append({"variable": var, "modalite": mod})
    return pd.DataFrame(rows)


# ─────────────────────────────────────────────────────────────────────────────
# 6. EXEMPLE D'UTILISATION
# ─────────────────────────────────────────────────────────────────────────────
reponses_exemple = {
        "statut_juridique":           "SARL",
        "region":                     "Littoral",
        "taille_entreprise":          "Petite Entreprise",
        "date_debut_activite":        "5 a 9 ans",
        "secteur_activite_princ":     "Agriculture et Agroalimentaire",
        "besoin_intrants":            "Oui",
        "besoin_financement":         "Oui",
        "besoin_emballages":          "Non",
        "besoin_transport":           "Oui",
        "besoin_appui_entreprise":    "Oui",
        "besoin_equipements":         "Non",
        "besoin_innovation_recherche":"Non",
    }

def coordonnees_entreprises(dictio):

    # ── 6a. Réponses d'un individu exemple ──────────────────────────────────
    

    # ── 6b. Construction du TDC (1 individu) ────────────────────────────────
    tdc_ligne = construire_tdc_individu(dictio)

    # Affichage du TDC sous forme de tableau condensé
    
    #print(tdc_ligne)
    #tdc_ligne.to_csv("tdc_individu_exemple.csv", index=False)
    # ── 6c. TDC pour plusieurs individus ────────────────────────────────────
    # 1. Chargement des fichiers fournis
    df_ind = tdc_ligne
    df_coords = pd.read_csv("mca_categories_coords.csv")
    df_eig = pd.read_csv("mca_eigenvalues.csv")

    # Nombre de variables qualitatives actives constatées dans ton profil (nombre de "1")
    Q = int(df_ind.sum(axis=1).values[0])
    print(f"Nombre de variables actives détectées (Q) : {Q}\n")

    # 2. Alignement du vecteur de l'individu (x) avec l'ordre des modalités de l'ACM
    x = np.zeros(len(df_coords))

    for i, mod in enumerate(df_coords["modalite"]):
        # Recherche de la colonne correspondante dans le tableau disjonctif complet
        # (gère le cas où FactoMineR a retiré le préfixe de la variable)
        matched_col = None
        for col in df_ind.columns:
            if col == mod or col.endswith("_" + str(mod)):
                matched_col = col
                break

        if matched_col is not None:
            x[i] = df_ind[matched_col].values[0]
        else:
            print(f"Attention : La modalité '{mod}' n'a pas été trouvée dans l'exemple.")

    # 3. Extraction des matrices de coordonnées (G) et des valeurs propres (lambdas)
    dimensions = [col for col in df_coords.columns if col.startswith("Dim")]
    G = df_coords[dimensions].values
    lambdas = df_eig["eigenvalue"].values[: len(dimensions)]

    # 4. Application de la formule de transition (Projection)
    # Somme des coordonnées des modalités actives (produit matriciel x . G)
    somme_ponderee = np.dot(x, G)

    # Normalisation par Q * racine_carree(valeurs_propres)
    coordonnees_projetees = somme_ponderee / (Q * np.sqrt(lambdas))

    # 5. Affichage des résultats
    #print("--- Coordonnées de l'individu sur les axes factoriels ---")
    resultats = dict(zip(dimensions, coordonnees_projetees))
    return resultats




   

