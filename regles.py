# Regles d'association  A -> B
#   support    = part des transactions qui contiennent A et B
#   confidence = support(A et B) / support(A)
#   lift       = confidence / support(B)   (> 1 : A et B vont souvent ensemble)

import pandas as pd


def generer_regles(frequents, min_confidence):
    regles = []

    for itemset in frequents:
        # A = un morceau plus petit de l'itemset (lui aussi frequent)
        for A in frequents:
            if len(A) >= len(itemset):
                continue

            A_dans_itemset = True
            for item in A:
                if item not in itemset:
                    A_dans_itemset = False
            if not A_dans_itemset:
                continue

            # B = le reste de l'itemset
            B = []
            for item in itemset:
                if item not in A:
                    B.append(item)
            B = tuple(B)

            confidence = frequents[itemset] / frequents[A]
            lift = confidence / frequents[B]

            if confidence >= min_confidence:
                regles.append({
                    "A": ", ".join(A),
                    "B": ", ".join(B),
                    "support": round(frequents[itemset], 3),
                    "confidence": round(confidence, 3),
                    "lift": round(lift, 2),
                })

    df = pd.DataFrame(regles, columns=["A", "B", "support", "confidence", "lift"])
    df = df.sort_values(["lift", "confidence", "support"], ascending=False)
    df = df.reset_index(drop=True)
    return df
