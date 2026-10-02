# Algorithme FP-Growth
# On range les transactions dans un arbre, puis on lit l'arbre.
# Un noeud de l'arbre est un simple dictionnaire :
#   {"item": ..., "compte": ..., "parent": ..., "enfants": {}}


def construire_arbre(transactions, min_compte):
    # transactions = liste de (liste d'items, poids)

    # 1) On compte chaque item
    compteurs = {}
    for items, poids in transactions:
        for item in items:
            if item in compteurs:
                compteurs[item] = compteurs[item] + poids
            else:
                compteurs[item] = poids

    # 2) On garde les items frequents, du plus frequent au moins frequent
    frequents = {}
    for item in compteurs:
        if compteurs[item] >= min_compte:
            frequents[item] = compteurs[item]
    ordre = sorted(frequents, key=lambda item: (-frequents[item], item))

    # 3) On ajoute chaque transaction dans l'arbre
    racine = {"item": None, "compte": 0, "parent": None, "enfants": {}}
    liens = {}   # pour chaque item : la liste des noeuds qui le portent
    for item in ordre:
        liens[item] = []

    for items, poids in transactions:
        noeud = racine
        for item in ordre:
            if item in items:
                if item not in noeud["enfants"]:
                    nouveau = {"item": item, "compte": 0, "parent": noeud, "enfants": {}}
                    noeud["enfants"][item] = nouveau
                    liens[item].append(nouveau)
                noeud = noeud["enfants"][item]
                noeud["compte"] = noeud["compte"] + poids

    return frequents, liens


def chercher_motifs(frequents, liens, suffixe, min_compte, resultat):
    for item in frequents:
        motif = tuple(sorted(suffixe + [item]))
        resultat[motif] = frequents[item]

        # On remonte l'arbre depuis chaque noeud de cet item
        chemins = []
        for noeud in liens[item]:
            chemin = []
            parent = noeud["parent"]
            while parent["item"] is not None:
                chemin.append(parent["item"])
                parent = parent["parent"]
            if len(chemin) > 0:
                chemins.append((chemin, noeud["compte"]))

        # On recommence avec ces chemins (petit arbre)
        if len(chemins) > 0:
            sous_frequents, sous_liens = construire_arbre(chemins, min_compte)
            chercher_motifs(sous_frequents, sous_liens, suffixe + [item], min_compte, resultat)


def fp_growth(transactions, min_support):
    total = len(transactions)
    min_compte = min_support * total

    # Au depart chaque transaction a un poids de 1
    liste = []
    for transaction in transactions:
        liste.append((transaction, 1))

    frequents, liens = construire_arbre(liste, min_compte)

    comptes = {}
    chercher_motifs(frequents, liens, [], min_compte, comptes)

    # On transforme les nombres en support (entre 0 et 1)
    resultat = {}
    for motif in comptes:
        resultat[motif] = comptes[motif] / total
    return resultat
