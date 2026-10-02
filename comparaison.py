import time
import pandas as pd

from lecture_logs import lire_fichier, creer_transactions
from apriori import apriori
from fp_growth import fp_growth
from regles import generer_regles

# Parametres
FICHIER = "data/sample_auth.log"   # ou "data/auth.log" (logs du Raspberry Pi)
MIN_SUPPORT = 0.1
MIN_CONFIDENCE = 0.6

# Pour afficher les tableaux en entier dans le terminal
pd.set_option("display.width", 200)
pd.set_option("display.max_columns", 10)

# --- Lecture des logs ---
df = lire_fichier(FICHIER)
print("Evenements SSH :", len(df))
print(df.head())

transactions = creer_transactions(df)
print("\nExemple de transaction :")
print(transactions[0])

# --- Apriori ---
debut = time.time()
motifs_apriori = apriori(transactions, MIN_SUPPORT)
temps_apriori = time.time() - debut

# --- FP-Growth ---
debut = time.time()
motifs_fp = fp_growth(transactions, MIN_SUPPORT)
temps_fp = time.time() - debut

# --- Regles d'association ---
regles_apriori = generer_regles(motifs_apriori, MIN_CONFIDENCE)
regles_fp = generer_regles(motifs_fp, MIN_CONFIDENCE)

# --- Comparaison ---
comparaison = pd.DataFrame({
    "Critere": ["Temps (ms)", "Motifs frequents", "Regles"],
    "Apriori": [round(temps_apriori * 1000, 2), len(motifs_apriori), len(regles_apriori)],
    "FP-Growth": [round(temps_fp * 1000, 2), len(motifs_fp), len(regles_fp)],
})
print("\nComparaison :")
print(comparaison)

if set(motifs_apriori) == set(motifs_fp):
    print("\nLes deux algorithmes trouvent les memes motifs.")
else:
    print("\nAttention : les motifs sont differents !")

print("\nTop 10 des regles (triees par lift) :")
print(regles_fp.head(10))
