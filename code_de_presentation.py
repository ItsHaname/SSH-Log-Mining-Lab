import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# 1. Les tickets de caisse
tickets = [
    ["Lait", "Pain", "Couches"],
    ["Lait", "Pain", "Couches", "Biere"],
    ["Pain", "Couches", "Biere"],
    ["Lait", "Pain", "Couches", "Biere"],
    ["Lait", "Pain"],
    ["Pain", "Couches"],
    ["Lait", "Couches", "Biere"],
    ["Lait", "Pain", "Couches"],
]

# 2. Transformer en tableau 0/1
te = TransactionEncoder()
df = pd.DataFrame(te.fit_transform(tickets), columns=te.columns_)

# 3. Trouver les itemsets fréquents (au moins 3 tickets sur 8)
itemsets = apriori(df, min_support=3/8, use_colnames=True)

# 4. Générer les règles (confiance >= 70%)
regles = association_rules(itemsets, metric="confidence", min_threshold=0.70)

# 5. Afficher les règles
print(regles[["antecedents", "consequents", "support", "confidence", "lift"]])
