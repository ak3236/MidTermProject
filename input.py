import pandas as pd
import os
from select_file import select_file

def read_transactions(file_path):
    transactions = pd.read_csv(file_path, header=None)
    #print("Transactions: ", transactions)
    return transactions

if __name__ == "__main__":
    selected_file = select_file()
    if selected_file:
        print(f"Selected database: {selected_file}")
        
        file_path = os.path.join(os.getcwd(), selected_file)
        transactions = read_transactions_from_file(file_path)
        print("Transactions read from file:")
        print(transactions)
