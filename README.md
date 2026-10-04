<h1 align="center">Lab — Apriori sur les logs SSH</h1>

<p align="center">
  <strong>Trouver des motifs fréquents et des règles d'association dans des logs SSH</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/pandas-150458?style=flat-square&logo=pandas&logoColor=white">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=flat-square&logo=streamlit&logoColor=white">
  <img src="https://img.shields.io/badge/SSH-222222?style=flat-square&logo=openssh&logoColor=white">
</p>

---

## Présentation

Ce lab applique l'algorithme **Apriori** aux logs d'authentification SSH d'un
Raspberry Pi. Une page Streamlit montre chaque étape de l'algorithme, puis les
règles d'association trouvées (par exemple : *« un utilisateur inexistant → mot de passe, la nuit »*).

Tout le code tient dans un seul fichier : `lab_apriori.py`.

---

## Structure

```text
SSH-Log-Mining-Lab/
├── lab_apriori.py         # le lab (lecture des logs + Apriori + règles + page Streamlit)
├── requirements.txt       # pandas, streamlit
└── data/
    ├── sample_auth.log    # logs d'exemple (attaques par force brute)
    └── auth.log           # vrais logs du Raspberry Pi
```

---

## Installation

```bash
git clone https://github.com/ItsHaname/SSH-Log-Mining-Lab.git
cd SSH-Log-Mining-Lab

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Lancer le lab

```bash
source .venv/bin/activate
streamlit run lab_apriori.py
```

La page s'ouvre sur `http://localhost:8501`. Dans la barre de gauche on choisit :

* le **fichier de logs** (`sample_auth.log` ou `auth.log`)
* le **support minimum**
* la **confiance minimum**

### Récupérer les logs du Raspberry Pi

```bash
ssh -i ~/.ssh/id_pi pi@192.168.50.2 "journalctl -u ssh --no-pager -o short" > data/auth.log
```

---

## Les étapes du lab

### Étape 0 — Du log à la transaction

Chaque ligne de log SSH devient une **transaction**, c'est-à-dire un ensemble d'items :

```text
Sep 16 01:18:38 raspberrypi sshd[1213]: Failed password for invalid user guest from 218.92.0.112 port 42398 ssh2
        ↓
{auth=password, event=failed_invalid_user, ip=218.92.0.112, period=night, status=failure, user=guest}
```

### Étapes 1, 2, 3… — Les itemsets fréquents

1. **Taille 1** : on calcule le support de chaque item seul et on garde ceux ≥ support minimum.
2. **Taille 2, 3…** : on combine les itemsets gardés pour créer les candidats de la taille suivante.
3. **Élagage (propriété Apriori)** : si un sous-groupe n'est pas fréquent, le groupe ne peut
   pas l'être non plus → il est éliminé **sans être compté**.
4. On s'arrête quand il n'y a plus de candidats.

### Dernière étape — Les règles A → B

Chaque itemset fréquent est coupé en deux parties A et B. On garde les règles avec
une confiance suffisante et un lift > 1, triées par lift.

| Mesure     | Formule                                    | Question posée                               |
| ---------- | ------------------------------------------ | -------------------------------------------- |
| Support    | nb transactions avec A et B / nb total     | Est-ce fréquent ?                            |
| Confiance  | support(A et B) / support(A)               | Quand je vois A, est-ce que je vois B ?      |
| Lift       | confiance / support(B)                     | A et B sont-ils vraiment liés ? (> 1 = oui)  |

---

## Résultats (support = 0.2, confiance = 0.8)

**Logs d'exemple** — 186 transactions, 4 tailles d'itemsets, 47 règles :

```text
{event=failed_invalid_user} → {auth=password, period=night, status=failure}
support = 0.3 | confiance = 0.95 | lift = 2.56
```

→ Les tentatives avec un utilisateur inexistant se font par mot de passe et **la nuit** :
c'est la signature d'une attaque par force brute automatisée.

**Logs du Raspberry Pi** — 103 transactions :

```text
{status=success} → {auth=publickey}   confiance = 1.0 | lift = 1.94
{auth=password}  → {status=failure}   confiance = 1.0 | lift = 2.06
```

→ Toutes les connexions réussies utilisent une clé SSH et toutes celles par mot de passe
échouent : on peut désactiver l'authentification par mot de passe sans risque.
