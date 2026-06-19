import numpy as np
import pandas as pd
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from pickle import dump, load
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report

# ==========================================================
# 1. INITIALISATION DU MODÈLE MIROIR (Au démarrage de l'app)
# ==========================================================
# Charger les coordonnées d'entraînement issues de R
df_train = pd.read_csv("coords_enpre.csv",sep=",")

# Séparer les dimensions de l'ACM (X) et la variable cible (y)
X_train = df_train.drop(columns=["classe"])
y_train = df_train["classe"]
X_train, X_test, y_train, y_test = train_test_split(X_train, y_train, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)
# Créer et entraîner le classifieur LDA (Équivalent exact de MASS::lda)
# Note : Si tu as utilisé MASS::qda, utilise QuadraticDiscriminantAnalysis()
#model_predictif = LinearDiscriminantAnalysis()
#model_predictif.fit(X_train, y_train)
#with open("model_predictif.pkl", "wb") as f:
#    dump(model_predictif, f)

#print("✅ Le modèle prédictif Python est entraîné et prêt !")


model = LogisticRegression(max_iter=1000)  # max_iter augmenté pour assurer la convergence
model.fit(X_train_scaled, y_train)

y_pred = model.predict(X_test_scaled)
accuracy = accuracy_score(y_test, y_pred)
print(f"Précision globale (Accuracy) : {accuracy:.2f}\n")
print("Rapport de classification détaillé :")
print(classification_report(y_test, y_pred))