"""Association rules and their support / confidence / lift."""

from itertools import combinations


def generate_rules(frequent_itemsets, min_confidence=0.6):
    """Build the rules A -> B that reach min_confidence.

    frequent_itemsets is the {frozenset: support} mapping returned by
    apriori() or fp_growth(). Returns a list of dicts sorted by lift.
    """
    rules = []
    for itemset, support in frequent_itemsets.items():
        if len(itemset) < 2:
            continue
        items = sorted(itemset)
        # Every non-empty proper subset can be the antecedent.
        for size in range(1, len(items)):
            for antecedent in combinations(items, size):
                antecedent = frozenset(antecedent)
                consequent = itemset - antecedent

                antecedent_support = frequent_itemsets.get(antecedent)
                consequent_support = frequent_itemsets.get(consequent)
                if not antecedent_support or not consequent_support:
                    continue

                confidence = support / antecedent_support
                if confidence < min_confidence:
                    continue

                rules.append({
                    "antecedent": antecedent,
                    "consequent": consequent,
                    "support": support,
                    "confidence": confidence,
                    "lift": confidence / consequent_support,
                })

    rules.sort(key=lambda rule: (rule["lift"], rule["confidence"], rule["support"]),
               reverse=True)
    return rules


def format_rule(rule):
    """Render a rule as '{a, b} -> {c}'."""
    left = ", ".join(sorted(rule["antecedent"]))
    right = ", ".join(sorted(rule["consequent"]))
    return "{" + left + "} -> {" + right + "}"


def rules_to_rows(rules):
    """Flatten rules into rows ready for a table or a CSV."""
    return [{
        "rule": format_rule(rule),
        "antecedent": ", ".join(sorted(rule["antecedent"])),
        "consequent": ", ".join(sorted(rule["consequent"])),
        "support": round(rule["support"], 4),
        "confidence": round(rule["confidence"], 4),
        "lift": round(rule["lift"], 4),
    } for rule in rules]
