import csv
import os
from sklearn.metrics import classification_report
from ..swear_core.core import SwearingCheck

input_text = []
is_profane = []

def import_csv_data():
    current_dir = os.path.dirname(__file__)
    csv_file_path = os.path.join(current_dir, 'parsed_test3_1.csv')
    
    with open(csv_file_path, mode='r', encoding='utf-8') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for row in csv_reader:
            input_text.append(row['messages'])
            is_profane.append(int(row['is_profane']))
            

if len(input_text) == 0:
    import_csv_data()
             
swear_filter = SwearingCheck(reg_pred=True, bins=3, stop_words=["питон"])

y_prob_pred = swear_filter.predict_proba(input_text)
y_pred = swear_filter.predict(input_text)

print(classification_report(y_pred, is_profane))
