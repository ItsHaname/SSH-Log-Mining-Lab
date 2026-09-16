# 🔐 Laboratoire d'analyse des logs SSH

## Fouille de motifs fréquents avec Apriori et FP-Growth

Projet de laboratoire en cybersécurité et en fouille de données visant à analyser les logs d'authentification SSH à l'aide des algorithmes **Apriori** et **FP-Growth**.

Le projet consiste à collecter des événements SSH depuis un Raspberry Pi, transformer les logs bruts en données transactionnelles, rechercher des motifs fréquents et générer des règles d'association. Les performances d'Apriori et de FP-Growth sont ensuite comparées sur des jeux de données de différentes tailles.

---

# 📌 Présentation du projet

Les systèmes informatiques génèrent un grand nombre de journaux d'événements (logs). Les logs d'authentification SSH contiennent notamment des informations sur les connexions réussies, les échecs d'authentification et les utilisateurs concernés.

L'objectif de ce laboratoire est d'étudier comment les techniques de **fouille de motifs fréquents** peuvent être appliquées à ces événements afin d'identifier des associations récurrentes.

Le fonctionnement général du projet est le suivant :
<img width="921" height="554" alt="image" src="https://github.com/user-attachments/assets/a9198e35-5ab1-4e2a-9e3e-6c016151b01b" />


```text
┌─────────────────────┐
│    Raspberry Pi     │
│    Serveur SSH      │
└──────────┬──────────┘
           │
           ▼
       Logs SSH
           │
           ▼
┌─────────────────────┐
│ Analyseur Python    │
│ (Parser)            │
└──────────┬──────────┘
           │
           ▼
      Transactions
           │
      ┌────┴────┐
      ▼         ▼
  Apriori   FP-Growth
      │         │
      └────┬────┘
           ▼
   Règles d'association
           │
           ▼
 Évaluation des performances
           │
           ▼
       Base SQLite
           │
           ▼
      Tableau de bord
```

---

# 🎯 Problématique

> **Comment les techniques de fouille de motifs fréquents peuvent-elles être appliquées aux logs d'authentification SSH afin d'identifier des associations récurrentes, et comment les algorithmes Apriori et FP-Growth se comportent-ils en termes de performances lorsque la taille des données augmente ?**

---

# 🎯 Objectifs

Les objectifs du projet sont les suivants :

* Mettre en place un environnement SSH contrôlé.
* Collecter des événements d'authentification SSH.
* Analyser et structurer les logs bruts.
* Transformer les événements en transactions.
* Appliquer l'algorithme Apriori.
* Appliquer l'algorithme FP-Growth.
* Identifier les motifs fréquents.
* Générer des règles d'association.
* Calculer le support, la confiance et le lift.
* Comparer Apriori et FP-Growth.
* Mesurer le temps d'exécution.
* Mesurer la consommation mémoire.
* Étudier l'influence de la taille du jeu de données sur les performances.
* Stocker les résultats des expériences.
* Présenter les résultats dans un tableau de bord interactif.

---

# 🏗️ Architecture du laboratoire

Le laboratoire est constitué principalement de deux machines.

## 💻 Machine d'analyse

### Arch Linux

Le poste Arch Linux est utilisé pour :

* effectuer les opérations SSH dans le laboratoire ;
* générer des événements contrôlés ;
* analyser les données ;
* développer les programmes Python ;
* exécuter Apriori et FP-Growth ;
* effectuer les expérimentations ;
* consulter le tableau de bord.

## 🍓 Machine cible

### Raspberry Pi

Le Raspberry Pi est utilisé comme :

* serveur SSH ;
* machine cible du laboratoire ;
* source des journaux d'authentification.

L'environnement est destiné à des expérimentations contrôlées et autorisées.

---

# 🔄 Chaîne de traitement des données

Le projet transforme progressivement les logs SSH bruts en données exploitables par les algorithmes de fouille de données.

## 1. Collecte des logs

Les événements SSH peuvent notamment contenir :

```text
Échec d'authentification
Connexion réussie
Utilisateur invalide
Ouverture de session
Fermeture de session
Adresse IP
Nom d'utilisateur
Date et heure
```

---

## 2. Analyse des logs avec Python

Le programme Python extrait les informations importantes :

```text
Date et heure
Adresse IP
Nom d'utilisateur
Type d'événement
Statut de l'authentification
```

Exemple :

```text
{
    "ip": "192.168.1.20",
    "utilisateur": "root",
    "evenement": "failed_login"
}
```

---

## 3. Transformation en transactions

Les événements structurés sont regroupés afin de construire des transactions.

Exemple :

```text
T1 = {SSH, failed_login, root}

T2 = {SSH, failed_login, admin}

T3 = {SSH, accepted_login, user}
```

Ces transactions constituent l'entrée des algorithmes de fouille de motifs.

---

# 🧠 Algorithme Apriori

Apriori est un algorithme de recherche de **motifs fréquents**.

Il fonctionne progressivement :

```text
1-itemsets
     ↓
2-itemsets
     ↓
3-itemsets
     ↓
...
```

À chaque étape, les ensembles qui ne respectent pas le support minimum sont supprimés.

Le principe fondamental d'Apriori est :

> **Si un itemset n'est pas fréquent, aucun itemset plus grand qui le contient ne peut être fréquent.**

Exemple :

```text
{SSH, failed_login}
```

peut être un motif fréquent.

Apriori peut ensuite rechercher :

```text
{SSH, failed_login, root}
```

si les conditions nécessaires sont satisfaites.

---

# 🌳 Algorithme FP-Growth

FP-Growth est également utilisé pour rechercher des motifs fréquents, mais son fonctionnement est différent d'Apriori.

Au lieu de générer de nombreux candidats, FP-Growth construit une structure appelée :

**FP-Tree (Frequent Pattern Tree)**

Le processus général est :

```text
Transactions
     ↓
Comptage des fréquences
     ↓
Construction du FP-Tree
     ↓
Bases de motifs conditionnelles
     ↓
Arbres conditionnels
     ↓
Motifs fréquents
```

L'objectif est de réduire le nombre de générations explicites de candidats nécessaires dans l'approche Apriori.

---

# 🔗 Règles d'association

Après l'identification des motifs fréquents, des règles d'association peuvent être générées.

Exemple :

```text
{SSH, failed_login} → {root}
```

Cette règle signifie que, dans les données étudiées, les transactions contenant `SSH` et `failed_login` contiennent également `root` avec une certaine fréquence.

Le symbole `→` indique une **association statistique** et non une relation de causalité.

---

# 📊 Mesures utilisées

## Support

Le support indique la fréquence d'apparition d'un ensemble d'éléments dans l'ensemble des transactions.

```text
Support(A → B)
= Support(A ∪ B)
```

---

## Confiance

La confiance indique la proportion de transactions contenant A qui contiennent également B.

```text
Confiance(A → B)
= Support(A ∪ B) / Support(A)
```

Exemple :

```text
{SSH, failed_login} → {root}

Confiance = 80 %
```

Cela signifie que, parmi les transactions contenant `SSH + failed_login`, `root` est également présent dans 80 % des cas.

---

## Lift

Le lift compare la confiance de la règle avec la fréquence générale de B.

```text
Lift(A → B)
= Confiance(A → B) / Support(B)
```

Interprétation générale :

```text
Lift > 1  → association positive
Lift = 1  → association approximativement indépendante
Lift < 1  → association négative
```

Ces mesures décrivent des associations statistiques dans les données. Elles ne permettent pas, à elles seules, d'affirmer qu'un événement constitue une attaque ou qu'une association est causale.

---

# ⚡ Comparaison Apriori / FP-Growth

Les deux algorithmes seront exécutés sur les mêmes jeux de données et avec des paramètres équivalents.

Plusieurs tailles de jeux de données pourront être utilisées :

```text
100 transactions
500 transactions
1 000 transactions
5 000 transactions
10 000 transactions
50 000 transactions
```

Pour chaque expérience, les métriques suivantes seront mesurées :

| Métrique             | Description                                                    |
| -------------------- | -------------------------------------------------------------- |
| Temps d'exécution    | Durée nécessaire à l'algorithme                                |
| Mémoire utilisée     | Quantité de mémoire consommée                                  |
| Motifs fréquents     | Nombre de motifs identifiés                                    |
| Règles d'association | Nombre de règles générées                                      |
| Support              | Fréquence des motifs                                           |
| Confiance            | Fréquence de la règle                                          |
| Lift                 | Force de l'association par rapport à la fréquence de référence |

---

# 🧪 Protocole expérimental

Pour assurer une comparaison correcte :

* les deux algorithmes utiliseront les mêmes transactions ;
* le même support minimum sera utilisé ;
* le même seuil de confiance sera utilisé pour la génération des règles ;
* les mêmes tailles de jeux de données seront testées ;
* les temps d'exécution seront mesurés ;
* la consommation mémoire sera mesurée ;
* les résultats seront enregistrés.

Exemple de configuration :

```yaml
support_minimum: 0.30
confiance_minimum: 0.60

jeux_de_donnees:
  - 100
  - 500
  - 1000
  - 5000
  - 10000
```

Les valeurs définitives seront déterminées lors de la phase expérimentale.

---

# 🗄️ Base de données

Une base **SQLite** peut être utilisée pour conserver les informations du laboratoire.

Elle pourra contenir plusieurs ensembles de données :

```text
logs
transactions
motifs_frequents
regles_association
experiences
performances
```

La base permet notamment de conserver l'historique des expériences et de fournir les données nécessaires au tableau de bord.

---

# 📊 Tableau de bord

Un tableau de bord interactif permettra de visualiser les résultats.

## Vue générale

```text
Nombre de logs
Nombre de transactions
Nombre de motifs fréquents
Nombre de règles
```

## Activité SSH

Visualisation de :

```text
Échecs d'authentification
Connexions réussies
Utilisateurs invalides
Autres événements SSH
```

## Règles d'association

Exemple :

```text
Règle :

{SSH, failed_login} → {root}

Support      : XX %
Confiance    : XX %
Lift         : X.XX
```

## Comparaison des algorithmes

Visualisation de :

```text
Apriori vs FP-Growth

Temps d'exécution
Consommation mémoire
Nombre de motifs
Nombre de règles
```

---

# 📁 Structure du projet

```text
ssh-log-mining-lab/
│
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
│
├── docs/
│   ├── architecture.md
│   ├── methodology.md
│   ├── apriori.md
│   ├── fp_growth.md
│   └── experimental_protocol.md
│
├── config/
│   └── config.yaml
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── samples/
│
├── src/
│   ├── parser/
│   ├── preprocessing/
│   ├── mining/
│   │   ├── apriori.py
│   │   ├── fp_growth.py
│   │   └── rules.py
│   ├── database/
│   └── evaluation/
│
├── experiments/
│   ├── run_apriori.py
│   ├── run_fp_growth.py
│   └── compare_algorithms.py
│
├── dashboard/
│   ├── app.py
│   ├── pages/
│   └── components/
│
├── tests/
│
├── results/
│   ├── tables/
│   └── figures/
│
└── scripts/
```

---

# 🛠️ Technologies

Les technologies envisagées sont :

* **Linux**
* **Raspberry Pi**
* **OpenSSH**
* **Python**
* **Pandas**
* **NumPy**
* **SQLite**
* **Apriori**
* **FP-Growth**
* **Matplotlib**
* **Streamlit**

Les bibliothèques pourront évoluer au cours du développement.

---

# 🚀 Installation

Cloner le dépôt :

```bash
git clone <URL-DU-DEPOT>
cd ssh-log-mining-lab
```

Créer un environnement virtuel Python :

```bash
python3 -m venv .venv
```

Activer l'environnement :

```bash
source .venv/bin/activate
```

Installer les dépendances :

```bash
pip install -r requirements.txt
```

---

# ▶️ Utilisation

Les différents composants pourront être exécutés séparément.

### Analyse des logs

```bash
python -m src.parser.ssh_log_parser
```

### Construction des transactions

```bash
python -m src.preprocessing.transactions
```

### Exécution d'Apriori

```bash
python experiments/run_apriori.py
```

### Exécution de FP-Growth

```bash
python experiments/run_fp_growth.py
```

### Comparaison

```bash
python experiments/compare_algorithms.py
```

### Lancement du tableau de bord

```bash
streamlit run dashboard/app.py
```

Les commandes définitives seront adaptées à l'implémentation finale.

---

# 🔬 Reproductibilité

Afin de rendre les expériences reproductibles :

* utiliser les mêmes données pour les deux algorithmes ;
* conserver les mêmes paramètres ;
* documenter la configuration ;
* enregistrer les résultats ;
* conserver les versions des bibliothèques ;
* mesurer les performances dans des conditions comparables.

---

# 🔐 Sécurité et éthique

Ce projet est destiné à un **environnement de laboratoire contrôlé et autorisé**.

Les expérimentations SSH doivent être réalisées uniquement sur les machines et réseaux autorisés.

Aucune donnée sensible ne doit être publiée dans le dépôt GitHub.

Le dépôt public doit utiliser :

* des données synthétiques ;
* des données anonymisées ;
* des exemples de logs ;
* aucune clé SSH privée ;
* aucun mot de passe ;
* aucune information personnelle sensible.

---

# 📌 État d'avancement

```text
[ ] Conception du laboratoire
[ ] Configuration du Raspberry Pi
[ ] Configuration du serveur SSH
[ ] Collecte des logs
[ ] Développement du parser
[ ] Transformation en transactions
[ ] Implémentation d'Apriori
[ ] Implémentation de FP-Growth
[ ] Génération des règles
[ ] Calcul du support
[ ] Calcul de la confiance
[ ] Calcul du lift
[ ] Benchmark des algorithmes
[ ] Base de données SQLite
[ ] Tableau de bord
[ ] Analyse des résultats
[ ] Documentation finale
```

---

# 🎓 Contexte académique

Ce projet est réalisé dans le cadre d'un travail académique portant sur l'association entre :

**Cybersécurité + Analyse des logs + Fouille de données**

L'objectif est d'étudier l'utilisation de techniques de fouille de motifs fréquents sur des événements d'authentification SSH et d'évaluer expérimentalement les différences entre Apriori et FP-Growth.

---

# 👤 Auteur

**Nom :** [Votre nom]

**Établissement :** [Nom de l'établissement]

**Formation :** [Nom de la formation]

**Année universitaire :** 2026–2027

---

# 📄 Licence

Projet destiné à des fins pédagogiques et de recherche.

Voir le fichier `LICENSE` pour les conditions d'utilisation.
