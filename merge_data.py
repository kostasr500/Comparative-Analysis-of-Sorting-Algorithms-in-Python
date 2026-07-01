import os
import glob
import pandas as pd

# 1. Βρίσκουμε όλα τα αρχεία στον τρέχοντα φάκελο που ξεκινάνε από 'results_'
file_list = glob.glob('results_*.csv')

all_data = []

for file in file_list:
    # 2. Αφαιρούμε το '.csv' και χωρίζουμε το όνομα.
    # Π.χ. από το 'results_1_best_1000' προκύπτει η λίστα: ['results', '1', 'best', '1000']
    parts = file.replace('.csv', '').split('_')
    
    # Το parts[1] (το σετ 1,2,3,4) το αγνοούμε εντελώς!
    input_case = parts[2].capitalize() # Παίρνει το 'best' και το κάνει 'Best'
    array_size = int(parts[3])         # Παίρνει το '1000' και το κάνει αριθμό
    
    # 3. Διαβάζουμε το CSV
    df = pd.read_csv(file)
    
    # 4. Προσθέτουμε τις νέες στήλες
    df['Array Size'] = array_size
    df['Input Case'] = input_case
    
    # 5. Μετονομάζουμε τη μνήμη για να είναι πιο καθαρός ο τίτλος
    df.rename(columns={'Peak Memory (KB)': 'Memory (KB)'}, inplace=True)
    
    all_data.append(df)

# 6. Ενώνουμε όλα τα δεδομένα και τα ταξινομούμε
final_df = pd.concat(all_data, ignore_index=True)
final_df = final_df[['Algorithm', 'Array Size', 'Input Case', 'Time (seconds)', 'Memory (KB)']]
final_df.sort_values(by=['Algorithm', 'Array Size', 'Input Case'], inplace=True)

# 7. Αποθηκεύουμε το τελικό αρχείο
#final_df.to_csv('final_dataset.csv', index=False)
final_df.to_csv('final_dataset.csv', index=False, na_rep='N/A')


print(f"Επιτυχία! Ενώθηκαν {len(file_list)} αρχεία σε ένα συνολικό 'final_dataset.csv' με {len(final_df)} γραμμές.")