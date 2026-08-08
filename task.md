# Tâches — Jumeau Numérique Prédictif — Fours Sécheurs de Phosphate (OCP)

Stage 1 mois — OCP Group, Direction de Bénéficiation, Sèchage Béni Idir, Khouribga
Digital Twin · Machine Learning · Optimisation de Procédé

## État actuel du projet

Baseline fonctionnel : génération de données synthétiques (4 345 lignes, Fév → Août 2026),
XGBoost de base (5 features, RMSE 0.55, R² 0.69), plot SHAP à l'écran.
Objectifs sujet : **RMSE < 15 kcal/t, R² > 0.91**.

Reste à faire : ~70 % du sujet (bilan enthalpique, API, Docker, OPC-UA, validation, livrables).

## Problèmes critiques identifiés

1. **Échelle de la cible** : le sujet fixe Cs = 800–1100 kcal/t, mais `datasetscript.py` génère
   9–12 → l'objectif RMSE < 15 kcal/t est inatteignable sur ces données. Corriger la génération.
2. **`src/api.py` manquant** : `docker-compose.yml` lance `uvicorn src.api:app` → le conteneur
   ne démarre pas.
3. **Conflit Docker/TkAgg** : `train_model_ocp.py` force `TkAgg` (fenêtre graphique) alors que le
   Dockerfile impose le backend headless `Agg` → crash de l'entraînement dans le conteneur.
4. **Chemins d'écriture** : les fichiers sont écrits dans le CWD au lieu de `data/` et `models/`
   (montés par docker-compose) → modèles jamais sauvegardés (`models/` vide).

## Architecture cible

```
data/ (données DCS ou synthétiques)
  → src/datasetscript.py (génération / nettoyage)
  → src/bilan_enthalpique.py (jumeau numérique, ODE)
  → src/train_model_ocp.py (XGBoost + SHAP) → models/
  → src/api.py (FastAPI : /predict_cs, /recommend_action)
  → Docker (docker-compose)
  → OPC-UA → OSIsoft PI System (push KPIs)
```

## Roadmap — étapes à suivre dans l'ordre

### Étape 1 — Nettoyage & cohérence des données (Semaine 1)

1. Corriger `datasetscript.py` :
   - écrire le CSV dans `data/` (pas le CWD) ;
   - passer `Cs_Fuel` à l'échelle réelle 800–1100 kcal/t ;
   - ajouter les variables du sujet : O₂, CO, T° flamme, humidité phosphate entrant,
     T° fumées sortie.
2. Créer `notebooks/01_eda_correlations.ipynb` : statistiques descriptives, séries temporelles,
   matrice de corrélation, détection des valeurs aberrantes.

### Étape 2 — Bilan enthalpique & modèle XGBoost (Semaine 2)

3. Implémenter le bilan enthalpique du four (ODE, Python) : enthalpies entrée/sortie, pertes,
   calcul théorique de la Cs_Fuel → c'est le « jumeau numérique » du sujet.
4. Feature engineering : décalages temporels (lag), moyennes glissantes, humidité,
   ratio air/fuel.
5. Optimiser XGBoost (GridSearch / RandomSearch, early stopping) avec **validation temporelle**
   (split chronologique, pas aléatoire). Objectifs : **RMSE < 15 kcal/t, R² > 0.91**.
6. Sauvegarder le modèle : `models/xgb_model.joblib` + fichier de métriques + liste des
   features utilisées.

### Étape 3 — SHAP, API FastAPI, Docker, OPC-UA (Semaine 3)

7. SHAP : sauvegarder `models/shap_summary.png` (backend Agg, sans fenêtre), identifier les
   5 leviers d'économie et formuler des recommandations chiffrées.
8. Créer `src/api.py` (FastAPI, Pydantic) :
   - `/predict_cs` : prédiction de la consommation spécifique ;
   - `/recommend_action` : recommandation de réglage basée sur l'analyse SHAP.
9. Corriger le Dockerfile : retirer l'override TkAgg, CMD = uvicorn (génération des données et
   entraînement en phase de build ou script séparé). `docker-compose.yml` pointe déjà vers
   `src.api:app`.
10. OPC-UA : pousser les KPIs (Cs prédite, RMSE, recommandations) vers OSIsoft PI System
    (client OPC-UA simulé en l'absence de DCS réel).

### Étape 4 — Validation, rapport, livrables (Semaine 4)

11. Backtest sur les 10 derniers jours : comparer prédictions vs réelles, ajuster le modèle.
12. Finaliser : README complet, notebooks documentés, rapport technique + présentation
    à l'équipe.

## Livrables attendus (sujet)

- Code source documenté (GitHub) + notebooks
- Modèle XGBoost validé + analyse SHAP
- API FastAPI déployée en Docker
- Rapport technique final + présentation

## Commandes de lancement

- Données : `python src/datasetscript.py` (ou données réelles DCS dans `data/`)
- Entraînement : `python src/train_model_ocp.py`
- API : `docker compose up --build` puis http://localhost:8000/docs
