#Abhiram Krishnam - ak3236

from input import select_file, read_transactions
from apriori import apply_apriori
from fp_growth import apply_fp_growth
from brute_force import find_association_rules

import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
import time

# Read transactions 
selected_file = select_file()
if selected_file:
    # Read the selected file
    dataset = pd.read_csv(selected_file)

    # Preprocess the dataset
    transactions = [transaction.split(',') for transaction in dataset['Transactions']]
    print("   TRANSACTIONS:   \n")
    print(transactions)
    te = TransactionEncoder()
    te_ary = te.fit_transform(transactions)
    dataSet = pd.DataFrame(te_ary, columns=te.columns_)

    # Enter support and confidence thresholds
    support = float(input("Enter the minimum support threshold (%): "))
    confidence = float(input("Enter the minimum confidence threshold (%): "))

    min_support = support / 100
    min_confidence = confidence / 100

    min_support_count = min_support * len(transactions)
    
    #Apriori algorithm
    print("\n   --- APRIORI ALGORITHM --- \n")
    start_time = time.time()
    frequent_itemsets_apriori, association_rules_apriori = apply_apriori(transactions, min_support, min_confidence)
    end_time = time.time()
    apriori_time = end_time - start_time
    print(f"Time taken by Apriori algorithm: {apriori_time:.6f} seconds \n")

    if association_rules_apriori is None:
        print("No association rules for the minimum confidence(Apriori).")
    else:
        print("Final Association rules (Apriori): \n")
        for i, rule in enumerate(association_rules_apriori.iterrows(), start=1):
            antecedent = list(rule[1]['antecedents'])
            consequent = list(rule[1]['consequents'])
            confidence = rule[1]['confidence']
            support = rule[1]['support']
            print(f"Rule {i}: {antecedent} -> {consequent}")
            print(f"Confidence: {confidence}") 
            print(f"Support: {support} \n")


    #FP-Growth algorithm
    print("\n   --- FP-GROWTH ALGORITHM ---\n")
    start_time = time.time()
    frequent_itemsets_fpgrowth, association_rules_fpgrowth = apply_fp_growth(transactions, min_support, min_confidence)
    end_time = time.time()
    fpgrowth_time = end_time - start_time
    print(f"Time taken by FP-Growth algorithm: {fpgrowth_time:.6f} seconds\n")

    if association_rules_fpgrowth is None:
        print("No association rules for the minimum confidence(FP-Growth).")
    else:
        print("Final Association rules (FP-Growth): \n")
        for i, rule in enumerate(association_rules_fpgrowth.iterrows(), start=1):
            antecedent = list(rule[1]['antecedents'])
            consequent = list(rule[1]['consequents'])
            confidence = rule[1]['confidence']
            support = rule[1]['support']
            print(f"Rule {i}: {antecedent} -> {consequent}")
            print(f"Confidence: {confidence}") 
            print(f"Support: {support} \n")


    #Brute Force algorithm
    print("\n   --- BRUTE FORCE ALGORITHM ---\n")
    start_time = time.time()
    frequent_itemsets, association_rules = find_association_rules(transactions, min_support, min_confidence)
    end_time = time.time()
    bruteforce_time = end_time - start_time
    print(f"Time taken by Brute Force algorithm: {bruteforce_time:.6f} seconds\n")

    if association_rules:
        print("Final Association Rules (Brute Force):")
        for i, rule in enumerate(association_rules, start=1):
            antecedent, consequent, support, confidence = rule
            print(f"Rule {i}: {antecedent} -> {consequent}")
            print(f"Confidence: {confidence :.2f}%")
            print(f"Support: {support :.2f}% \n")
    else:
        print("\nNo association rules for the minimum confidence(Brute Force).")
