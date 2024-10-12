from itertools import combinations

def generate_itemsets(transactions, min_support):
    min_support_value = min_support
    #print(f"Minimum Support Value in generate_itemsets: {min_support_value}")
    itemsets = {}
    for transaction in transactions:
        itemset = frozenset(transaction)
        itemsets[itemset] = itemsets.get(itemset, 0) + 1

    # print("Itemsets and Their Counts:")
    # print(itemsets)

    unique_items = set()
    for itemset in itemsets.keys():
        unique_items.update(itemset)

    frequent_itemsets = []
    candidate_itemsets = [frozenset([item]) for item in unique_items]
    # print("Initial Candidate Itemsets:", candidate_itemsets)

    k = 1
    while candidate_itemsets:
        #print(f"\nCurrent Candidate Itemsets (Length {k}):", candidate_itemsets)
        if k == 1:
            frequent_candidates = [itemset for itemset in candidate_itemsets if sum(1 for transaction in transactions if itemset.issubset(transaction)) >= min_support_value * len(transactions)]
        else:
            frequent_candidates = []
            for candidate in candidate_itemsets:
                support_count = sum(1 for transaction in transactions if set(candidate).issubset(set(transaction)))
                if support_count >= min_support_value * len(transactions):
                    frequent_candidates.append(candidate)
        # print(f"Frequent Candidates (Length {k}):", frequent_candidates)
        frequent_itemsets.extend(frequent_candidates)

        if not frequent_candidates:
            break

        candidate_itemsets = generate_candidate_itemsets(frequent_candidates, unique_items, k)
        k += 1

    return frequent_itemsets

def generate_candidate_itemsets(frequent_itemsets, unique_items, k):
    candidate_itemsets = []
    for i in range(len(frequent_itemsets)):
        itemset1 = frequent_itemsets[i]
        for j in range(i + 1, len(frequent_itemsets)):
            itemset2 = frequent_itemsets[j]
            candidate_itemset = itemset1.union(itemset2)
            if len(candidate_itemset) == k + 1 and candidate_itemset not in candidate_itemsets:
                candidate_itemsets.append(candidate_itemset)
    return candidate_itemsets



def generate_all_subsets(itemset):
    return [frozenset(subset) for length in range(1, len(itemset)) for subset in combinations(itemset, length)]

def calculate_confidence(antecedent, consequent, transactions):
    antecedent_count = sum(1 for transaction in transactions if antecedent.issubset(transaction))
    #print(f"Antecedent Count for {antecedent} -> {consequent}: {antecedent_count}")
    consequent_count = sum(1 for transaction in transactions if (antecedent | consequent).issubset(transaction))
    #print(f"Consequent Count for {antecedent} -> {consequent}: {consequent_count}")
    confidence = (consequent_count / antecedent_count) * 100 if antecedent_count > 0 else 0
    return confidence



def find_association_rules(transactions, min_support, min_confidence):
    # print(f"Minimum Support Value association: {min_support}")
    frequent_itemsets = generate_itemsets(transactions, min_support)
    # print("Frequent Itemsets:")
    # print(frequent_itemsets)
    association_rules = []

    for itemset in frequent_itemsets:
        if len(itemset) > 1:
            for antecedent in generate_all_subsets(itemset):
                consequent = itemset - antecedent
                #print(f"Antecedent: {antecedent}, Consequent: {consequent}")
                support = sum(1 for transaction in transactions if itemset.issubset(transaction)) / len(transactions)
                confidence = calculate_confidence(antecedent, consequent, transactions)
                # print(f"Rule: {list(antecedent)} -> {list(consequent)}, Confidence: {confidence:.2f}%")
                # print(f"Support: {support * 100:.2f}%")

                if confidence >= min_confidence:
                    association_rules.append((list(antecedent), list(consequent), support * 100, confidence))

    return frequent_itemsets, association_rules