import os

def select_file():
    # List CSV files 
    csv_files = [file for file in os.listdir() if file.endswith('.csv')]
    
    if not csv_files:
        print("No CSV files found in the current directory.")
        return None
    
    print("Select a store:")
    for i, file in enumerate(csv_files, start=1):
        file_name = os.path.splitext(file)[0]
        print(f"{i}. {file_name}")

    choice = input("Select a store number: ")

    try:
        index = int(choice) - 1
        if 0 <= index < len(csv_files):
            return csv_files[index]
        else:
            print("Invalid choice. Please enter a number corresponding to a store.")
            return select_file()  
    except ValueError:
        print("Invalid choice. Please enter a number corresponding to a store.")
        return select_file()  

if __name__ == "__main__":
    selected_file = select_file()
    if selected_database:
        print(f"Selected file: {selected_file}")
