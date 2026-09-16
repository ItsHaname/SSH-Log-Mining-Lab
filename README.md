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

Les deux algorithmes seront exécutés sur les **mêmes données** et avec les mêmes paramètres afin de permettre une comparaison cohérente.

Les critères étudiés sont notamment :

| Critère                    |   Apriori | FP-Growth |
| -------------------------- | --------: | --------: |
| Temps d'exécution          | À mesurer | À mesurer |
| Nombre de motifs fréquents | À mesurer | À mesurer |
| Nombre de règles           | À mesurer | À mesurer |
| Consommation mémoire       | À mesurer | À mesurer |

Les résultats seront obtenus expérimentalement au cours du laboratoire.

---

## Structure du projet

```text
mini-lab/
│
├── README.md
│
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
