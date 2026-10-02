# Lecture des logs SSH
# Une ligne de log  ->  un evenement  ->  une transaction (liste d'items)

import pandas as pd


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
