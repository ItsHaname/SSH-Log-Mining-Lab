"""Compare Apriori and FP-Growth on the same transactions.

Usage:
    python experiments/compare.py [log_file] [min_support] [min_confidence]
"""

import os
import sys
import time
import tracemalloc

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.apriori import apriori
from src.fp_growth import fp_growth
from src.parser import load_transactions
from src.rules import format_rule, generate_rules

DEFAULT_LOG = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                           "data", "sample_auth.log")


def benchmark(algorithm, transactions, min_support, min_confidence, repeats=5):
    """Run one algorithm and measure its time, memory and output size."""
    tracemalloc.start()
    best = None
    for _ in range(repeats):
        start = time.perf_counter()
        itemsets = algorithm(transactions, min_support)
        elapsed = time.perf_counter() - start
        best = elapsed if best is None else min(best, elapsed)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    rules = generate_rules(itemsets, min_confidence)
    return {
        "name": algorithm.__name__,
        "time": best,
        "memory": peak / 1024,
        "itemsets": itemsets,
        "rules": rules,
    }


def main():
    log_file = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_LOG
    min_support = float(sys.argv[2]) if len(sys.argv) > 2 else 0.1
    min_confidence = float(sys.argv[3]) if len(sys.argv) > 3 else 0.6

    transactions = load_transactions(log_file)
    print(f"Log          : {log_file}")
    print(f"Transactions : {len(transactions)}")
    print(f"min_support  : {min_support}   min_confidence : {min_confidence}")
    print()

    results = [
        benchmark(apriori, transactions, min_support, min_confidence),
        benchmark(fp_growth, transactions, min_support, min_confidence),
    ]

    header = f"{'Critere':<28}" + "".join(f"{r['name']:>14}" for r in results)
    print(header)
    print("-" * len(header))
    rows = [
        ("Temps d'execution (ms)", lambda r: f"{r['time'] * 1000:.2f}"),
        ("Memoire pic (Ko)", lambda r: f"{r['memory']:.1f}"),
        ("Motifs frequents", lambda r: str(len(r["itemsets"]))),
        ("Regles d'association", lambda r: str(len(r["rules"]))),
    ]
    for label, value in rows:
        print(f"{label:<28}" + "".join(f"{value(r):>14}" for r in results))
    print()

    same = results[0]["itemsets"].keys() == results[1]["itemsets"].keys()
    print(f"Memes motifs frequents : {'oui' if same else 'NON'}")
    faster, slower = sorted(results, key=lambda r: r["time"])
    ratio = slower["time"] / faster["time"] if faster["time"] else float("inf")
    print(f"Plus rapide            : {faster['name']} (x{ratio:.2f})")
    print()

    print("Top 10 regles (triees par lift)")
    print("-" * 78)
    print(f"{'Regle':<52}{'supp':>8}{'conf':>8}{'lift':>8}")
    for rule in results[1]["rules"][:10]:
        text = format_rule(rule)
        text = text if len(text) <= 51 else text[:48] + "..."
        print(f"{text:<52}{rule['support']:>8.3f}"
              f"{rule['confidence']:>8.3f}{rule['lift']:>8.2f}")


if __name__ == "__main__":
    main()
