# 🔐 Mini-Lab — SSH Log Mining

## 📌 Description

Mini-laboratoire permettant d'analyser des **logs d'authentification SSH** et d'appliquer deux algorithmes de fouille de motifs fréquents :

* **Apriori**
* **FP-Growth**

L'objectif est d'identifier des **motifs fréquents** et des **règles d'association**, puis de comparer les performances des deux algorithmes.

---

## 🏗️ Architecture

```text
Raspberry Pi
     │
     ▼
   SSH Logs
     │
     ▼
 Python Parser
     │
     ▼
 Transactions
     │
 ┌───┴────┐
 ▼        ▼
Apriori  FP-Growth
 │        │
 └───┬────┘
     ▼
Comparaison
     │
     ▼
 Dashboard
```

---

## 🎯 Objectifs

* Collecter des logs SSH.
* Transformer les logs en transactions.
* Appliquer Apriori.
* Appliquer FP-Growth.
* Générer des règles d'association.
* Calculer :

  * Support
  * Confidence
  * Lift
* Comparer les performances des deux algorithmes.

---

## 🧠 Exemple

Une transaction peut être représentée ainsi :

```text
T1 = {SSH, failed_login, root}
```

Une règle d'association peut être :

```text
{SSH, failed_login} → {root}
```

Les règles sont évaluées avec le **support**, la **confidence** et le **lift**.

---

## 📊 Comparaison

Les deux algorithmes seront exécutés sur les mêmes données afin de comparer notamment :

* Temps d'exécution
* Nombre de motifs fréquents
* Nombre de règles
* Consommation mémoire

---

## 📁 Structure

```text
mini-lab/
│
├── README.md
├── data/
│   └── logs.csv
│
├── src/
│   ├── parser.py
│   ├── apriori.py
│   ├── fp_growth.py
│   └── rules.py
│
├── experiments/
│   └── compare.py
│
└── dashboard/
    └── app.py
```

---

## 🛠️ Technologies

* Linux
* Raspberry Pi
* SSH
* Python
* Apriori
* FP-Growth
* Streamlit

---

## 🔐 Utilisation

Ce laboratoire est destiné à des **expérimentations contrôlées et autorisées** dans un environnement de test.

---

## 👤 Auteur

**Nom :*AIT BAH hanane*

**Formation :**NSC

**Établissement :** FSSM

**Année :** 2026–2027
