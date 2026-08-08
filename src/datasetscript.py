import pandas as pd
import numpy as np

print("🔄 Génération du dataset OCP pour Février → Août 2026...")

# 1. Création de la base de temps (Du 1er Février 2026 au 1er Août 2026, heure par heure)
dates = pd.date_range(start='2026-02-01', end='2026-08-01', freq='h')
hours = len(dates)

print(f"📅 {hours} heures générées (Février à Août 2026).")

np.random.seed(42)  # Pour des résultats reproductibles

# 2. Génération des paramètres (plages conformes au sujet OCP)
# Débit Produit Brut (60 - 520 t/h)
debit_produit = 250 + 200 * np.sin(np.arange(hours) / 100) + np.random.normal(0, 30, hours)
debit_produit = np.clip(debit_produit, 60, 520)

# Débit Fuel (1000 - 3200 t/h) - corrélé au débit produit
debit_fuel = 2000 + 500 * (debit_produit - 250) / 200 + np.random.normal(0, 100, hours)
debit_fuel = np.clip(debit_fuel, 1000, 3200)

# O2 dans les fumées (3 - 8 %)
o2 = 5.5 + 1.2 * np.sin(np.arange(hours) / 160) + np.random.normal(0, 0.6, hours)
o2 = np.clip(o2, 3, 8)

# CO dans les fumées (0 - 500 ppm) - corrélé négativement à O2
co = 250 - 60 * (o2 - 5.5) + 30 * np.sin(np.arange(hours) / 190) + np.random.normal(0, 40, hours)
co = np.clip(co, 0, 500)

# Température Flamme (1200 - 1600 °C) - corrélée au débit fuel
temp_flamme = 1400 + 0.15 * (debit_fuel - 2000) + 30 * np.sin(np.arange(hours) / 180) + np.random.normal(0, 15, hours)
temp_flamme = np.clip(temp_flamme, 1200, 1600)

# Humidité Phosphate entrant (10 - 20 %)
humidite = 15 + 4 * np.sin(np.arange(hours) / 170) + np.random.normal(0, 1.5, hours)
humidite = np.clip(humidite, 10, 20)

# Température Fumées sortie (100 - 140 °C) - corrélée au débit fuel
temp_fumees = 120 + 15 * np.sin(np.arange(hours) / 210) + 0.02 * (debit_fuel - 2000) + np.random.normal(0, 4, hours)
temp_fumees = np.clip(temp_fumees, 100, 140)

# Température Buse (750 - 980°C)
temp_buse = 850 + 100 * np.sin(np.arange(hours) / 150) + np.random.normal(0, 20, hours)
temp_buse = np.clip(temp_buse, 750, 980)

# Cs Fuel (Conso spécifique) (800 - 1100 kcal/t) - dépendante du process
# Humidité ↑ → Cs ↑ · Débit produit ↑ → économie d'échelle → Cs ↓
# Temp fumées ↑ → pertes ↑ → Cs ↑ · Temp buse ↑ → meilleure combustion → Cs ↓
cs_fuel = (
    950
    + 45 * np.sin(np.arange(hours) / 250)                     # tendance lente
    - 0.05 * (debit_produit - 250)                            # économie d'échelle
    + 2.5 * (humidite - 15)                                   # humidité entrant
    + 1.0 * (temp_fumees - 120)                               # pertes fumées
    + 0.25 * (temp_buse - 850)                                # combustion
    + 3.0 * (o2 - 5.5)                                        # excès d'air
    + np.random.normal(0, 7.5, hours)                         # bruit de mesure
)
cs_fuel = np.clip(cs_fuel, 800, 1100)

# Température Chambre (60 - 95°C)
temp_chambre = 75 + 15 * np.sin(np.arange(hours) / 200) + np.random.normal(0, 5, hours)
temp_chambre = np.clip(temp_chambre, 60, 95)

# Température Entrée Filtre (60 - 95°C)
temp_entree_filtre = temp_chambre + np.random.normal(0, 2, hours)
temp_entree_filtre = np.clip(temp_entree_filtre, 60, 95)

# Température Sortie Filtre (80 - 90°C)
temp_sortie_filtre = 85 + 4 * np.sin(np.arange(hours) / 250) + np.random.normal(0, 2, hours)
temp_sortie_filtre = np.clip(temp_sortie_filtre, 80, 90)

# Température Brique (200 - 350°C)
temp_brique = 280 + 50 * np.sin(np.arange(hours) / 180) + np.random.normal(0, 10, hours)
temp_brique = np.clip(temp_brique, 200, 350)

# Température Tôle (60 - 120°C)
temp_tole = 90 + 25 * np.sin(np.arange(hours) / 220) + np.random.normal(0, 8, hours)
temp_tole = np.clip(temp_tole, 60, 120)

# Dépression (-1.5 à -15 mBar)
depression = -8 + 5 * np.sin(np.arange(hours) / 130) + np.random.normal(0, 1.5, hours)
depression = np.clip(depression, -15, -1.5)

# Delta P Filtre (40 - 130 mmCE)
delta_p_filtre = 85 + 35 * np.sin(np.arange(hours) / 300) + np.random.normal(0, 10, hours)
delta_p_filtre = np.clip(delta_p_filtre, 40, 130)

# Pression d'air Filtre (3 - 7.5 bar)
pression_air = 5 + 1.5 * np.sin(np.arange(hours) / 200) + np.random.normal(0, 0.5, hours)
pression_air = np.clip(pression_air, 3, 7.5)

# Courant Virole (80 - 100 A)
courant_virole = 90 + 8 * np.sin(np.arange(hours) / 250) + np.random.normal(0, 3, hours)
courant_virole = np.clip(courant_virole, 80, 100)

# Poussière (50 - 100 mg/m³)
poussiere = 75 + 20 * np.sin(np.arange(hours) / 180) + np.random.normal(0, 10, hours)
poussiere = np.clip(poussiere, 50, 100)

# 3. Assemblage du DataFrame
df = pd.DataFrame({
    'Date': dates,
    'Debit_Produit_Brut': debit_produit,      # t/h
    'Debit_Fuel': debit_fuel,                  # t/h
    'Cs_Fuel': cs_fuel,                        # Conso spécifique (CIBLE) en kcal/t
    'Temp_Buse': temp_buse,                    # °C
    'Temp_Chambre': temp_chambre,              # °C
    'Temp_Entree_Filtre': temp_entree_filtre,  # °C
    'Temp_Sortie_Filtre': temp_sortie_filtre,  # °C
    'Temp_Brique': temp_brique,                # °C
    'Temp_Toile': temp_tole,                   # °C
    'Depression': depression,                  # mBar
    'Delta_P_Filtre': delta_p_filtre,          # mmCE
    'Pression_Air_Filtre': pression_air,       # bar
    'Courant_Virole': courant_virole,          # A
    'Poussiere': poussiere,                    # mg/m³
    'O2': o2,                                  # % (fumées)
    'CO': co,                                  # ppm (fumées)
    'Temp_Flamme': temp_flamme,                # °C
    'Humidite_Phosphate': humidite,            # %
    'Temp_Fumees_Sortie': temp_fumees          # °C
})

# 4. Sauvegarde dans data/
import os
os.makedirs('data', exist_ok=True)
df.to_csv('data/donnees_four_ocp_2026.csv', index=False)
print(f"✅ Dataset généré avec succès ! {len(df)} lignes (Fév → Août 2026).")
print("📁 Fichier : 'data/donnees_four_ocp_2026.csv'")
print("\n📊 Aperçu des 5 premières lignes :")
print(df.head())

print("\n📈 Récapitulatif des plages générées :")
print(df.describe())
