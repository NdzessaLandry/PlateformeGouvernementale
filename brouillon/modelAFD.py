import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from pickle import dump, load

# ==========================================================
# 1. INITIALISATION DU MODÈLE MIROIR (Au démarrage de l'app)
# ==========================================================
# Charger les coordonnées d'entraînement issues de R
df_train = pd.read_csv("coords_enpre.csv",sep=",")

# Séparer les dimensions de l'ACM (X) et la variable cible (y)
X_train = df_train.drop(columns=["classe"])
y_train = df_train["classe"]

# Créer et entraîner le classifieur LDA (Équivalent exact de MASS::lda)
# Note : Si tu as utilisé MASS::qda, utilise QuadraticDiscriminantAnalysis()
model_predictif = LinearDiscriminantAnalysis()
model_predictif.fit(X_train, y_train)
with open("model_predictif.pkl", "wb") as f:
    dump(model_predictif, f)

print("✅ Le modèle prédictif Python est entraîné et prêt !")