import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
import shap
import matplotlib
matplotlib.use('TkAgg')  # Force l'ouverture de la fenêtre graphique
import matplotlib.pyplot as plt
import os

print("="*50)
print("🚀 LANCEMENT DU MODELE XGBOOST - FOUR OCP")
print("="*50)

# 1. Vérifier que le fichier est bien là
fichier = 'data/donnees_four_ocp_2026.csv'
if not os.path.exists(fichier):
    print(f"❌ Erreur : Le fichier '{fichier}' est introuvable.")
    print("📁 Assure-toi que datasetscript.py a bien généré ce fichier.")
    exit()

print(f"📂 Chargement du dataset : {fichier}")
df = pd.read_csv(fichier)
print(f"✅ {len(df)} lignes chargées avec succès !")

# 2. Sélection des variables (features) et de la cible (target)
# On garde les variables les plus logiques pour prédire la consommation
features = [
    'Debit_Produit_Brut', 
    'Debit_Fuel', 
    'Temp_Buse', 
    'Temp_Chambre', 
    'Depression'
]
target = 'Cs_Fuel'

print("\n🔍 Variables d'entrée (X) :")
for f in features:
    print(f"   - {f}")
print(f"🎯 Variable à prédire (y) : {target}")

X = df[features]
y = df[target]

# 3. Division en entraînement (80%) et test (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
print(f"\n📊 Données d'entraînement : {len(X_train)} lignes")
print(f"📊 Données de test : {len(X_test)} lignes")

# 4. Entraînement du modèle XGBoost
print("\n🧠 Entraînement du modèle XGBoost...")
model = xgb.XGBRegressor(
    n_estimators=100, 
    enable_categorical=False,
    random_state=42
)
model.fit(X_train, y_train)

# 5. Évaluation des performances
predictions = model.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, predictions))
print(f"\n📈 Performance du modèle : RMSE = {rmse:.4f}")
print("   (Plus le RMSE est petit, plus le modèle est précis)")

# 6. Génération du graphique SHAP (LE LIVRABLE IMPORTANT)
print("\n📊 Génération du graphique SHAP...")
print("   ⏳ Une fenêtre graphique va s'ouvrir dans quelques secondes...")

# Création de l'explainer SHAP
explainer = shap.TreeExplainer(model, X_train, feature_perturbation='tree_path_dependent')
shap_values = explainer.shap_values(X_test)

# Affichage du graphique (la fameuse fenêtre)
shap.summary_plot(shap_values, X_test, show=True)

print("\n✅ Graphique SHAP affiché avec succès !")
print("🎉 Tu peux fermer la fenêtre graphique pour terminer le script.")
print("="*50)