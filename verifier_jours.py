import pandas as pd

# Charge le fichier
df = pd.read_csv('donnees_four_ocp_2026.csv')
df['Date'] = pd.to_datetime(df['Date'])

# 1. Vérifie le nombre de jours
nb_jours = df['Date'].dt.date.nunique()
print(f"📅 Nombre total de jours dans le fichier : {nb_jours} jours")

# 2. Affiche un aperçu des 5 premiers jours (moyenne par jour)
print("\n📊 Aperçu des 5 premiers jours (moyenne de la consommation 'Cs_Fuel') :")
print(df.groupby(df['Date'].dt.date)['Cs_Fuel'].mean().head())

# 3. Vérifie qu'il y a bien 24 points (heures) par jour
print("\n⏳ Vérification du nombre de points par jour (derniers jours) :")
print(df.groupby(df['Date'].dt.date).size().tail())

# 4. Affiche l'écart (min/max) de la consommation
print("\n📈 Consommation (Cs_Fuel) par jour - Statistiques :")
print(df.groupby(df['Date'].dt.date)['Cs_Fuel'].agg(['min', 'max', 'mean']).head(10))