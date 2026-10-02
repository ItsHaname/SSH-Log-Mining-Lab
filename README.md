<h1 align="center">Mini-Lab — SSH Log Mining</h1>

<p align="center">
  <strong>Analyse de logs SSH et fouille de motifs fréquents</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Linux-000000?style=flat-square&logo=linux&logoColor=white">
  <img src="https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/SSH-222222?style=flat-square&logo=openssh&logoColor=white">
  <img src="https://img.shields.io/badge/Apriori-Research-blue?style=flat-square">
  <img src="https://img.shields.io/badge/FP--Growth-Research-purple?style=flat-square">
</p>

---

## Présentation

Ce mini-laboratoire permet d'analyser des **logs d'authentification SSH** et d'appliquer deux algorithmes de fouille de motifs fréquents :

* **Apriori**
* **FP-Growth**

L'objectif est d'identifier des **motifs fréquents** et des **règles d'association**, puis de comparer les performances des deux algorithmes sur les mêmes données.

---

## Architecture

<p align="center">
  <img src="https://github.com/user-attachments/assets/8f323c20-b2f2-40b9-9e3f-641d6ec66edb" width="850">
</p>

<p align="center">
  <strong>Raspberry Pi → SSH Logs → Python Parser → Transactions → Apriori / FP-Growth → Comparaison → Dashboard</strong>
</p>

---

## Objectifs

Le laboratoire a pour objectifs de :

1. Collecter des logs SSH.
2. Transformer les logs en transactions.
3. Appliquer l'algorithme **Apriori**.
4. Appliquer l'algorithme **FP-Growth**.
5. Générer des règles d'association.
6. Calculer les métriques :

   * Support
   * Confidence
   * Lift
7. Comparer les performances des deux algorithmes.

---

## Exemple

Une transaction peut être représentée sous la forme :

```text
T1 = {SSH, failed_login, root}
```

À partir des transactions, une règle d'association peut être générée :

```text
{SSH, failed_login} → {root}
```

Les règles sont évaluées à l'aide de trois mesures principales :

| Mesure     | Description                                    |
| ---------- | ---------------------------------------------- |
| Support    | Fréquence d'apparition d'un ensemble d'items   |
| Confidence | Probabilité d'observer B lorsque A est présent |
| Lift       | Mesure de l'association entre A et B           |

---

## Comparaison des algorithmes

Les deux algorithmes sont exécutés sur les **mêmes données** et avec les mêmes
paramètres. Résultats sur le log d'exemple (186 transactions,
`MIN_SUPPORT = 0.1`, `MIN_CONFIDENCE = 0.6`) :

| Critère                    | Apriori  | FP-Growth |
| -------------------------- | -------: | --------: |
| Temps d'exécution          | ~10-16 ms |    ~1 ms |
| Nombre de motifs fréquents |       95 |        95 |
| Nombre de règles           |      169 |       169 |

Les deux algorithmes trouvent **exactement les mêmes motifs fréquents**.
FP-Growth est beaucoup plus rapide car il ne génère pas de candidats : il range
les transactions dans un arbre et lit l'arbre.

---

## Installation

```bash
git clone https://github.com/ItsHaname/SSH-Log-Mining-Lab.git
cd SSH-Log-Mining-Lab

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Seules deux bibliothèques sont utilisées : **pandas** et **streamlit**.

---

## Utilisation

### 1. Comparer Apriori et FP-Growth

```bash
python comparaison.py
```

Les paramètres se changent directement en haut du fichier :

```python
FICHIER = "data/sample_auth.log"
MIN_SUPPORT = 0.1
MIN_CONFIDENCE = 0.6
```

### 2. Lancer le dashboard

```bash
streamlit run dashboard.py
```

Le dashboard s'ouvre sur `http://localhost:8501`. Le fichier de log, le support
et la confiance se règlent dans la barre de gauche.

### 3. Utiliser les fonctions directement

```python
from lecture_logs import lire_fichier, creer_transactions
from fp_growth import fp_growth
from regles import generer_regles

df = lire_fichier("data/sample_auth.log")
transactions = creer_transactions(df)

motifs = fp_growth(transactions, 0.1)
regles = generer_regles(motifs, 0.6)
print(regles.head())
```

---

## Des logs aux transactions

Chaque ligne SSH reconnue devient **une transaction**. Le parser extrait le type
d'événement, l'utilisateur, l'IP source, la méthode d'authentification, le
résultat et la période de la journée.

```text
Sep 16 01:18:38 raspberrypi sshd[1213]: Failed password for invalid user guest from 218.92.0.112 port 42398 ssh2
```

devient :

```text
{event=failed_invalid_user, status=failure, period=night,
 user=guest, ip=218.92.0.112, auth=password}
```

Les événements reconnus sont : `failed_password`, `failed_invalid_user`,
`accepted`, `invalid_user`, `connection_closed` et `disconnected`. Les lignes
qui ne concernent pas `sshd` sont ignorées.

Les périodes sont : `night` (0h-6h), `morning` (6h-12h), `afternoon` (12h-18h)
et `evening` (18h-0h).

---

## Résultats sur le log d'exemple

Le log d'exemple contient 186 événements SSH : une attaque par force brute la
nuit et des connexions légitimes en journée. Les règles les plus fortes
retrouvent bien ce comportement :

```text
{event=accepted}                -> {status=success}          supp=0.102  conf=1.000  lift=9.79
{auth=password, user=root}      -> {event=failed_password}    supp=0.118  conf=1.000  lift=8.09
{user=root}                     -> {event=failed_password}    supp=0.118  conf=0.759  lift=6.13
```

Lecture : un lift nettement supérieur à 1 signifie que les deux membres de la
règle apparaissent ensemble bien plus souvent que ne le voudrait le hasard.

---

## Logs du Raspberry Pi

Le fichier `data/sample_auth.log` est un **log d'exemple**. Pour analyser les
vrais logs du Raspberry Pi :

```bash
# Raspberry Pi OS récent (Bookworm) : les logs SSH sont dans journalctl
ssh <utilisateur>@<ip_du_pi> "journalctl -u ssh --no-pager -o short" > data/auth.log

# Raspberry Pi OS plus ancien : le fichier auth.log existe
scp <utilisateur>@<ip_du_pi>:/var/log/auth.log data/auth.log
```

Ensuite, dans `comparaison.py`, mettre `FICHIER = "data/auth.log"` (ou taper
`data/auth.log` dans la barre de gauche du dashboard).

---

## Structure du projet

```text
SSH-Log-Mining-Lab/
│
├── README.md
├── requirements.txt
│
├── data/
│   └── sample_auth.log      # log SSH d'exemple
│
├── lecture_logs.py          # log -> événements (DataFrame) -> transactions
├── apriori.py               # Apriori
├── fp_growth.py             # FP-Growth
├── regles.py                # règles + support / confidence / lift
├── comparaison.py           # comparaison Apriori vs FP-Growth
└── dashboard.py             # dashboard Streamlit
```

---

## Technologies

<p align="center">
  <img src="https://skillicons.dev/icons?i=linux,python" height="55">
</p>

* Linux
* Raspberry Pi
* SSH
* Python
* Apriori
* FP-Growth
* Streamlit

---

## Flux de traitement

```text
SSH Authentication Logs
          │
          ▼
     Python Parser
          │
          ▼
      Transactions
          │
     ┌────┴────┐
     ▼         ▼
 Apriori    FP-Growth
     │         │
     └────┬────┘
          ▼
 Frequent Patterns
          │
          ▼
 Association Rules
          │
          ▼
 Support / Confidence / Lift
          │
          ▼
    Performance
    Comparison
          │
          ▼
       Dashboard
```

---

## Auteur

<table>
  <tr>
    <td><strong>Nom</strong></td>
    <td>AIT BAH Hanane</td>
  </tr>
  <tr>
    <td><strong>Formation</strong></td>
    <td>NSC</td>
  </tr>
  <tr>
    <td><strong>Établissement</strong></td>
    <td>FSSM</td>
  </tr>
  <tr>
    <td><strong>Année</strong></td>
    <td>2026–2027</td>
  </tr>
</table>

---

<p align="center">
  <sub>Mini-Lab académique — SSH Log Mining</sub>
</p>
