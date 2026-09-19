"""Streamlit dashboard for the SSH log mining lab.

Run with:
    streamlit run dashboard/app.py
"""

import os
import sys
import time

import pandas as pd
import streamlit as st

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.apriori import apriori
from src.fp_growth import fp_growth
from src.parser import parse_file, to_transactions
from src.rules import generate_rules, rules_to_rows

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_LOG = os.path.join(ROOT, "data", "sample_auth.log")

st.set_page_config(page_title="SSH Log Mining", layout="wide")
st.title("Mini-Lab — SSH Log Mining")

# --- Sidebar: data source and parameters ------------------------------------
st.sidebar.header("Parametres")
uploaded = st.sidebar.file_uploader("Fichier de log (auth.log)", type=None)
min_support = st.sidebar.slider("Support minimum", 0.01, 0.5, 0.10, 0.01)
min_confidence = st.sidebar.slider("Confiance minimum", 0.1, 1.0, 0.60, 0.05)

if uploaded is not None:
    log_path = os.path.join(ROOT, "data", "_uploaded.log")
    with open(log_path, "wb") as handle:
        handle.write(uploaded.getbuffer())
    source = uploaded.name
else:
    log_path = DEFAULT_LOG
    source = "data/sample_auth.log (exemple)"

st.sidebar.caption(f"Source : {source}")

# --- Parsing ----------------------------------------------------------------
events = parse_file(log_path)
transactions = to_transactions(events)

if not transactions:
    st.error("Aucun evenement SSH reconnu dans ce fichier.")
    st.stop()

events_df = pd.DataFrame(events)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Evenements", len(events))
col2.metric("Echecs", int((events_df["status"] == "failure").sum()))
col3.metric("Succes", int((events_df["status"] == "success").sum()))
col4.metric("IP distinctes", events_df["ip"].nunique())

tab_logs, tab_patterns, tab_rules, tab_compare = st.tabs(
    ["Logs", "Motifs frequents", "Regles d'association", "Apriori vs FP-Growth"]
)

# --- Tab 1: parsed logs -----------------------------------------------------
with tab_logs:
    st.subheader("Evenements analyses")
    st.dataframe(events_df, width="stretch", height=300)

    left, right = st.columns(2)
    with left:
        st.caption("Evenements par type")
        st.bar_chart(events_df["event"].value_counts())
    with right:
        st.caption("Top 10 des IP sources")
        st.bar_chart(events_df["ip"].value_counts().head(10))

    st.caption("Exemple de transactions")
    st.write([", ".join(transaction) for transaction in transactions[:5]])

# --- Mining -----------------------------------------------------------------
start = time.perf_counter()
apriori_itemsets = apriori(transactions, min_support)
apriori_time = time.perf_counter() - start

start = time.perf_counter()
fp_itemsets = fp_growth(transactions, min_support)
fp_time = time.perf_counter() - start

rules = generate_rules(fp_itemsets, min_confidence)

# --- Tab 2: frequent itemsets ----------------------------------------------
with tab_patterns:
    st.subheader(f"Motifs frequents (support >= {min_support:.2f})")
    patterns_df = pd.DataFrame([
        {
            "itemset": ", ".join(sorted(itemset)),
            "taille": len(itemset),
            "support": round(support, 4),
        }
        for itemset, support in fp_itemsets.items()
    ]).sort_values(["taille", "support"], ascending=[True, False])
    st.write(f"{len(patterns_df)} motifs trouves")
    st.dataframe(patterns_df, width="stretch", height=400)

# --- Tab 3: association rules ----------------------------------------------
with tab_rules:
    st.subheader(f"Regles d'association (confiance >= {min_confidence:.2f})")
    if not rules:
        st.warning("Aucune regle avec ces parametres. Baissez le support ou la confiance.")
    else:
        rules_df = pd.DataFrame(rules_to_rows(rules))
        st.write(f"{len(rules_df)} regles trouvees")
        st.dataframe(
            rules_df[["rule", "support", "confidence", "lift"]],
            width="stretch", height=400,
        )
        st.caption("Top 10 regles par lift")
        top = rules_df.head(10).set_index("rule")["lift"]
        st.bar_chart(top)
        st.download_button(
            "Telecharger les regles (CSV)",
            rules_df.to_csv(index=False).encode("utf-8"),
            file_name="association_rules.csv",
            mime="text/csv",
        )

# --- Tab 4: algorithm comparison -------------------------------------------
with tab_compare:
    st.subheader("Comparaison des deux algorithmes")
    same = apriori_itemsets.keys() == fp_itemsets.keys()
    comparison = pd.DataFrame({
        "Critere": ["Temps d'execution (ms)", "Motifs frequents", "Regles d'association"],
        "Apriori": [
            round(apriori_time * 1000, 2),
            len(apriori_itemsets),
            len(generate_rules(apriori_itemsets, min_confidence)),
        ],
        "FP-Growth": [
            round(fp_time * 1000, 2),
            len(fp_itemsets),
            len(rules),
        ],
    })
    st.dataframe(comparison, width="stretch", hide_index=True)

    if same:
        st.success("Les deux algorithmes trouvent exactement les memes motifs frequents.")
    else:
        st.error("Les deux algorithmes ne trouvent pas les memes motifs.")

    faster = "FP-Growth" if fp_time < apriori_time else "Apriori"
    ratio = max(apriori_time, fp_time) / min(apriori_time, fp_time)
    st.info(f"Le plus rapide sur ce jeu de donnees : **{faster}** (x{ratio:.2f})")
    st.bar_chart(pd.DataFrame(
        {"temps (ms)": [apriori_time * 1000, fp_time * 1000]},
        index=["Apriori", "FP-Growth"],
    ))
