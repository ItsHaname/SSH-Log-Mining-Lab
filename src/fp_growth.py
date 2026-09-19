"""FP-Growth: frequent itemset mining with a prefix tree, without candidates."""


class FPNode:
    """One node of the FP-tree."""

    def __init__(self, item, parent):
        self.item = item
        self.count = 0
        self.parent = parent
        self.children = {}
        self.link = None  # next node holding the same item


def _build_header(transactions, min_count):
    """Count single items and keep only the frequent ones."""
    counts = {}
    for transaction in transactions:
        for item in set(transaction):
            counts[item] = counts.get(item, 0) + 1
    return {item: count for item, count in counts.items() if count >= min_count}


def _insert(node, items, count, headers):
    """Insert one ordered transaction into the tree."""
    for item in items:
        child = node.children.get(item)
        if child is None:
            child = FPNode(item, node)
            node.children[item] = child
            # Chain the node into the header table's linked list.
            head = headers[item]
            if head["node"] is None:
                head["node"] = child
            else:
                tail = head["node"]
                while tail.link is not None:
                    tail = tail.link
                tail.link = child
        child.count += count
        node = child


def _build_tree(transactions, min_count):
    """Build an FP-tree and its header table from weighted transactions."""
    item_counts = {}
    for transaction, count in transactions:
        for item in set(transaction):
            item_counts[item] = item_counts.get(item, 0) + count
    frequent = {item: count for item, count in item_counts.items() if count >= min_count}
    if not frequent:
        return None, {}

    # Most frequent first; the item name breaks ties so the order is stable.
    order = sorted(frequent, key=lambda item: (-frequent[item], item))
    rank = {item: i for i, item in enumerate(order)}
    headers = {item: {"count": frequent[item], "node": None} for item in order}

    root = FPNode(None, None)
    for transaction, count in transactions:
        items = sorted({item for item in transaction if item in frequent},
                       key=lambda item: rank[item])
        if items:
            _insert(root, items, count, headers)
    return root, headers


def _prefix_paths(headers, item):
    """Collect the conditional pattern base of an item."""
    paths = []
    node = headers[item]["node"]
    while node is not None:
        path = []
        parent = node.parent
        while parent is not None and parent.item is not None:
            path.append(parent.item)
            parent = parent.parent
        if path:
            paths.append((path, node.count))
        node = node.link
    return paths


def _mine(headers, suffix, min_count, frequent):
    """Recursively mine the tree described by its header table."""
    # Least frequent item first, as FP-Growth requires.
    for item in sorted(headers, key=lambda i: (headers[i]["count"], i)):
        pattern = frozenset(suffix) | {item}
        frequent[pattern] = headers[item]["count"]

        conditional = _prefix_paths(headers, item)
        if not conditional:
            continue
        _, sub_headers = _build_tree(conditional, min_count)
        if sub_headers:
            _mine(sub_headers, pattern, min_count, frequent)


def fp_growth(transactions, min_support=0.1):
    """Return {frozenset(itemset): support} for every frequent itemset.

    min_support is a ratio between 0 and 1.
    """
    total = len(transactions)
    if total == 0:
        return {}

    min_count = min_support * total
    if not _build_header(transactions, min_count):
        return {}

    weighted = [(transaction, 1) for transaction in transactions]
    _, headers = _build_tree(weighted, min_count)
    if not headers:
        return {}

    counts = {}
    _mine(headers, frozenset(), min_count, counts)
    return {itemset: count / total for itemset, count in counts.items()}
