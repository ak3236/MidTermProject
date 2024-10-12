import pandas as pd
from mlxtend.frequent_patterns import fpgrowth, association_rules

def apply_fp_growth(trans_data, support_threshold, conf_threshold):
    # Convert list of transactions to DataFrame and apply one-hot encoding
    encoded_data = pd.get_dummies(pd.DataFrame(trans_data).stack()).groupby(level=0).sum()
    encoded_data = encoded_data.astype(bool)
    
    freq_itemsets = fpgrowth(encoded_data, min_support=support_threshold, use_colnames=True)
    
    if freq_itemsets.empty:
        print("No frequent itemsets found with the specified minimum support threshold.")
        return None, None
    
    assoc_rules = association_rules(freq_itemsets, metric="confidence", min_threshold=conf_threshold)
    
    # Convert confidence and support values to formatted strings with "%" symbol
    assoc_rules['confidence'] = assoc_rules['confidence'].apply(lambda x: '{:.2f}%'.format(x * 100))
    assoc_rules['support'] = assoc_rules['support'].apply(lambda x: '{:.2f}%'.format(x * 100))
    
    if assoc_rules.empty:
        return freq_itemsets, None
    
    return freq_itemsets, assoc_rules
