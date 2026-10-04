# Lab Apriori sur les logs SSH
# Lancer avec :  streamlit run lab_apriori.py

import pandas as pd
import streamlit as st


# ============ Lecture des logs SSH ============
# Une ligne de log  ->  un evenement  ->  une transaction (liste d'items)

def moment_de_la_journee(heure):
    if heure < 6:
        return "night"
    elif heure < 12:
        return "morning"
    elif heure < 18:
        return "afternoon"
    else:
        return "evening"


def lire_ligne(ligne):
    # Exemple de ligne :
    # Sep 16 01:18:38 raspberrypi sshd[1213]: Failed password for root from 1.2.3.4 port 5678 ssh2
    mots = ligne.split()

    # On garde seulement les lignes de sshd
    if len(mots) < 8 or "sshd" not in mots[4]:
        return None

    heure = int(mots[2].split(":")[0])
    message = " ".join(mots[5:])

    # Quel type d'evenement ?
    if message.startswith("Accepted"):
        event = "accepted"
    elif message.startswith("Failed") and "invalid user" in message:
        event = "failed_invalid_user"
    elif message.startswith("Failed"):
        event = "failed_password"
    elif message.startswith("Invalid user"):
        event = "invalid_user"
    elif message.startswith("Connection closed by authenticating user"):
        event = "connection_closed"
    elif message.startswith("Disconnected from invalid user"):
        event = "disconnected"
    else:
        return None   # ligne qui ne nous interesse pas

    if "port" not in mots:
        return None

    # Le nom d'utilisateur
    if event == "accepted" or event == "failed_password":
        user = mots[mots.index("for") + 1]   # "... for root from ..."
    else:
        user = mots[mots.index("user") + 1]  # "... user admin from ..."

    # L'adresse IP est toujours juste avant le mot "port"
    ip = mots[mots.index("port") - 1]

    # La methode (password / publickey) pour Accepted et Failed
    if mots[5] == "Accepted" or mots[5] == "Failed":
        auth = mots[6]
    else:
        auth = ""

    if event == "accepted":
        status = "success"
    else:
        status = "failure"

    return {
        "date": mots[0] + " " + mots[1],
        "heure": mots[2],
        "event": event,
        "status": status,
        "user": user,
        "ip": ip,
        "auth": auth,
        "period": moment_de_la_journee(heure),
    }


def lire_fichier(chemin):
    # Renvoie un DataFrame : une ligne par evenement SSH
    evenements = []
    fichier = open(chemin, "r", errors="replace")
    for ligne in fichier:
        evenement = lire_ligne(ligne)
        if evenement is not None:
            evenements.append(evenement)
    fichier.close()
    return pd.DataFrame(evenements)


def creer_transactions(df):
    # Chaque evenement devient une liste d'items, ex : ['event=accepted', 'user=pi', ...]
    transactions = []
    for i in range(len(df)):
        ligne = df.iloc[i]
        items = []
        items.append("event=" + ligne["event"])
        items.append("status=" + ligne["status"])
        items.append("period=" + ligne["period"])
        items.append("user=" + ligne["user"])
        items.append("ip=" + ligne["ip"])
        if ligne["auth"] != "":
            items.append("auth=" + ligne["auth"])
        transactions.append(sorted(items))
    return transactions


st.title("Lab — Apriori sur les logs SSH")

# --- Parametres (barre de gauche) ---
fichier = st.sidebar.selectbox("Fichier de logs", ["data/sample_auth.log", "data/auth.log"])
min_support = st.sidebar.slider("Support minimum", 0.05, 0.5, 0.20)
min_confiance = st.sidebar.slider("Confiance minimum", 0.5, 1.0, 0.80)


# ============ Etape 0 : les transactions ============
st.header("Etape 0 : du log a la transaction")
st.write("Chaque ligne de log SSH devient un ensemble d'items.")

df = lire_fichier(fichier)
transactions = []
for items in creer_transactions(df):
    transactions.append(set(items))

st.write("Nombre de transactions :", len(transactions))
st.dataframe(pd.DataFrame({"transaction": [", ".join(sorted(t)) for t in transactions[:10]]}))


def support(itemset):
    # Part des transactions qui contiennent TOUS les items de l'itemset
    compte = 0
    for transaction in transactions:
        if itemset.issubset(transaction):
            compte = compte + 1
    return compte / len(transactions)


def afficher(itemset):
    return "{" + ", ".join(sorted(itemset)) + "}"


# ============ Etapes 1, 2, 3... : les itemsets frequents ============
st.header("Etapes 1, 2, 3... : les itemsets frequents")
st.write("On garde les itemsets avec support >= ", min_support,
         ". Propriete Apriori : si un sous-groupe n'est pas frequent, "
         "le groupe est elimine sans etre compte (elagage).")

frequents_tous = {}   # {itemset: support}

# Candidats de taille 1 = chaque item seul
candidats = []
for transaction in transactions:
    for item in transaction:
        if frozenset([item]) not in candidats:
            candidats.append(frozenset([item]))

taille = 1
while len(candidats) > 0:
    st.subheader("Taille " + str(taille))

    # 1. On compte le support de chaque candidat
    lignes = []
    frequents = []
    for candidat in candidats:
        s = support(candidat)
        if s >= min_support:
            resultat = "garde"
            frequents.append(candidat)
            frequents_tous[candidat] = s
        else:
            resultat = "rejete"
        lignes.append({"itemset": afficher(candidat), "support": round(s, 2), "resultat": resultat})

    tableau = pd.DataFrame(lignes).sort_values("support", ascending=False)
    st.write(len(candidats), "candidats ->", len(frequents), "gardes")
    st.dataframe(tableau)

    # 2. On combine les itemsets gardes pour faire la taille suivante
    taille = taille + 1
    nouveaux = []
    for a in frequents:
        for b in frequents:
            c = a | b
            if len(c) == taille and c not in nouveaux:
                nouveaux.append(c)

    # 3. Elagage : chaque sous-groupe (on enleve 1 item) doit etre frequent
    candidats = []
    elagues = 0
    for c in nouveaux:
        ok = True
        for item in c:
            if c - {item} not in frequents:
                ok = False
        if ok:
            candidats.append(c)
        else:
            elagues = elagues + 1
    if elagues > 0:
        st.info(str(elagues) + " candidats de taille " + str(taille) + " elagues sans etre comptes")


# ============ Dernière etape : les regles ============
st.header("Derniere etape : les regles A -> B")
st.write("confiance = support(A et B) / support(A)  —  lift = confiance / support(B)  (> 1 : A et B sont lies)")

regles = []
for itemset in frequents_tous:
    for A in frequents_tous:
        # A doit etre un morceau plus petit de l'itemset
        if len(A) < len(itemset) and A.issubset(itemset):
            B = itemset - A
            confiance = frequents_tous[itemset] / frequents_tous[A]
            lift = confiance / frequents_tous[B]
            if confiance >= min_confiance and lift > 1:
                regles.append({
                    "A": afficher(A),
                    "B": afficher(B),
                    "support": round(frequents_tous[itemset], 2),
                    "confiance": round(confiance, 2),
                    "lift": round(lift, 2),
                })

if len(regles) == 0:
    st.warning("Aucune regle : baissez le support ou la confiance.")
else:
    regles = pd.DataFrame(regles).sort_values("lift", ascending=False)
    st.write(len(regles), "regles trouvees (triees par lift)")
    st.dataframe(regles)
    st.bar_chart(regles.head(10).set_index("A")["lift"])
