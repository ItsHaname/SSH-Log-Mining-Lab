"""Apriori: frequent itemset mining by breadth-first candidate generation."""

from itertools import combinations


def _count_candidates(transactions, candidates):
    """Count how many transactions contain each candidate itemset."""
    counts = {candidate: 0 for candidate in candidates}
    for transaction in transactions:
        items = set(transaction)
        for candidate in candidates:
            if items.issuperset(candidate):
                counts[candidate] += 1
    return counts


def _join(previous, size):
    """Build candidates of the given size from the frequent itemsets of size-1."""
    candidates = set()
    ordered = sorted(previous)
    for i, left in enumerate(ordered):
        for right in ordered[i + 1:]:
            union = left | right
            if len(union) != size:
                continue
            # Prune: every subset of size-1 must itself be frequent.
            if all(frozenset(sub) in previous
                   for sub in combinations(sorted(union), size - 1)):
                candidates.add(frozenset(union))
    return candidates


def apriori(transactions, min_support=0.1):
    """Return {frozenset(itemset): support} for every frequent itemset.

    min_support is a ratio between 0 and 1.
    """
    total = len(transactions)
    if total == 0:
        return {}

    min_count = min_support * total
    frequent = {}

    # Level 1: single items.
    singles = {frozenset([item]) for transaction in transactions for item in transaction}
    counts = _count_candidates(transactions, singles)
    current = {itemset for itemset, count in counts.items() if count >= min_count}
    for itemset in current:
        frequent[itemset] = counts[itemset] / total

    # Levels 2..n: join, count, prune.
    size = 2
    while current:
        candidates = _join(current, size)
        if not candidates:
            break
        counts = _count_candidates(transactions, candidates)
        current = {itemset for itemset, count in counts.items() if count >= min_count}
        for itemset in current:
            frequent[itemset] = counts[itemset] / total
        size += 1

    return frequent
