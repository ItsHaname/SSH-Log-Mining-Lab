# Algorithme Apriori
# On cherche les groupes d'items frequents : d'abord taille 1, puis 2, puis 3...
# Un itemset est un tuple trie, ex : ('event=failed_password', 'user=root')


def contient(transaction, itemset):
    # Vrai si tous les items de l'itemset sont dans la transaction
    for item in itemset:
        if item not in transaction:
            return False
    return True


def apriori(transactions, min_support):
    total = len(transactions)
    frequents = {}   # resultat : {itemset: support}

    # Etape 1 : les candidats de taille 1 = tous les items
    candidats = []
    for transaction in transactions:
        for item in transaction:
            if (item,) not in candidats:
                candidats.append((item,))

    taille = 1
    while len(candidats) > 0:

        # On compte chaque candidat
        gardes = []
        for candidat in candidats:
            compte = 0
            for transaction in transactions:
                if contient(transaction, candidat):
                    compte = compte + 1

            support = compte / total
            if support >= min_support:
                gardes.append(candidat)
                frequents[candidat] = support

        # On combine les itemsets gardes pour faire la taille suivante
        taille = taille + 1
        candidats = []
        for a in gardes:
            for b in gardes:
                nouveau = sorted(set(a + b))
                nouveau = tuple(nouveau)
                if len(nouveau) == taille and nouveau not in candidats:
                    candidats.append(nouveau)

    return frequents
