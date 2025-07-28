"""
Author: Partha Pratim Ray
Contact: parthapratimray1986@gmail.com
Date: 28/07/2025

This script performs flattening and cleaning of the Disease-Symptom dataset 
based on the original Disease-Symptom Knowledge Base available at:
https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html

The raw dataset used is sourced from:
https://raw.githubusercontent.com/anujdutt9/Disease-Prediction-from-Symptoms/master/notebook/dataset/raw_data.xlsx

Functionality:
- Loads the disease-symptom dataset from the specified URL
- Cleans unwanted junk characters
- Flattens composite disease codes (separated by ^) into individual rows
- Outputs a clean, analysis-ready CSV for further use

"""

import pandas as pd
import re

# Download Excel file directly from GitHub RAW link
file_url = 'https://raw.githubusercontent.com/anujdutt9/Disease-Prediction-from-Symptoms/master/notebook/dataset/raw_data.xlsx'
df = pd.read_excel(file_url)

# Fill down Disease names
df['Disease'] = df['Disease'].ffill()

# Drop 'Count of Disease Occurrence' if exists
if 'Count of Disease Occurrence' in df.columns:
    df = df.drop(columns=['Count of Disease Occurrence'])

# Remove rows where Symptom is NaN
df = df[df['Symptom'].notna()]

# Replace '^' with ',' in symptoms
df['Symptom'] = df['Symptom'].str.replace('^', ',', regex=False)

# --- Remove junk symbols like Â etc. from Disease and Symptom ---
def clean_text(text):
    # Remove any character that is not printable ASCII or common punctuation/space
    return re.sub(r'[^\x20-\x7E]', '', str(text))

df['Disease'] = df['Disease'].apply(clean_text)
df['Symptom'] = df['Symptom'].apply(clean_text)

# Prepare new rows for disease splits
expanded_rows = []

for disease, group in df.groupby('Disease', sort=False):
    symptoms = ','.join(group['Symptom'])
    disease_codes = [d.strip() for d in disease.split('^')]
    for code in disease_codes:
        expanded_rows.append({'Disease': code, 'Symptom': symptoms})

# Create result DataFrame preserving order
result = pd.DataFrame(expanded_rows)

# (Optional) Clean junk symbols from the final result again, just in case
result['Disease'] = result['Disease'].apply(clean_text)
result['Symptom'] = result['Symptom'].apply(clean_text)

# Save to CSV
output_csv = 'flattened_url.csv'
result.to_csv(output_csv, index=False)

result.head()
