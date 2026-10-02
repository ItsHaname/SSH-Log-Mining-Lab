# Lancer avec :  streamlit run dashboard.py

import time
import pandas as pd
import streamlit as st

from lecture_logs import lire_fichier, creer_transactions
from apriori import apriori
from fp_growth import fp_growth
from regles import generer_regles

st.title("Mini-Lab — SSH Log Mining")

# --- Parametres (barre de gauche) ---
fichier = st.sidebar.text_input("Fichier de log", "data/sample_auth.log")
min_support = st.sidebar.slider("Support minimum", 0.01, 0.5, 0.10)
min_confidence = st.sidebar.slider("Confiance minimum", 0.1, 1.0, 0.60)

# --- Lecture des logs ---
df = lire_fichier(fichier)
if len(df) == 0:
    st.error("Aucun evenement SSH trouve dans ce fichier.")
    st.stop()

transactions = creer_transactions(df)

st.header("1. Les logs SSH")
st.write("Nombre d'evenements :", len(df))
st.dataframe(df)
st.bar_chart(df["event"].value_counts())
st.write("Top 10 des adresses IP :")
st.bar_chart(df["ip"].value_counts().head(10))

# --- Apriori et FP-Growth ---
debut = time.time()
motifs_apriori = apriori(transactions, min_support)
temps_apriori = time.time() - debut

debut = time.time()
motifs_fp = fp_growth(transactions, min_support)
temps_fp = time.time() - debut

st.header("2. Motifs frequents")
motifs = pd.DataFrame({
    "itemset": [", ".join(m) for m in motifs_fp],
    "support": [round(s, 3) for s in motifs_fp.values()],
})
st.write("Nombre de motifs :", len(motifs))
st.dataframe(motifs.sort_values("support", ascending=False))

st.header("3. Regles d'association")
regles = generer_regles(motifs_fp, min_confidence)
st.write("Nombre de regles :", len(regles))
st.dataframe(regles)

st.header("4. Apriori vs FP-Growth")
comparaison = pd.DataFrame({
    "Critere": ["Temps (ms)", "Motifs frequents", "Regles"],
    "Apriori": [round(temps_apriori * 1000, 2), len(motifs_apriori),
                len(generer_regles(motifs_apriori, min_confidence))],
    "FP-Growth": [round(temps_fp * 1000, 2), len(motifs_fp), len(regles)],
})
st.dataframe(comparaison)

if set(motifs_apriori) == set(motifs_fp):
    st.success("Les deux algorithmes trouvent les memes motifs.")
else:
    st.error("Les motifs sont differents !")
