# Disease-Symptom Data Cleaner and Flattener

This repository provides a Python script for cleaning, normalizing, and flattening disease-symptom datasets Unified Medical Language System [(UMLS)][https://www.nlm.nih.gov/research/umls/index.html] specific [https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html](https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html).
It is designed to process medical data from Excel files (especially those with composite codes separated by `^`), remove unwanted junk characters, and output a clean, analysis-ready CSV.

## Features

* **Directly loads medical data** from a GitHub-hosted Excel file
* **Fills missing disease names** using last valid entry (forward fill)
* **Removes unnecessary columns** (e.g., occurrence counts)
* **Eliminates rows with missing symptoms**
* **Handles composite disease codes**: splits codes joined by `^` into separate records
* **Removes junk characters** (e.g., `Â`) from disease and symptom columns
* **Exports a clean, flattened CSV** ready for ML or analytics

## Input

"raw_data.xlsx" The script loads raw data which is obtained in .xlsx format from [https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html](https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html) from below github link:

```
https://raw.githubusercontent.com/anujdutt9/Disease-Prediction-from-Symptoms/master/notebook/dataset/raw_data.xlsx
```

## Output

A cleaned and flattened CSV named:

```
flattened_url.csv
```

Each row contains a single disease code and its associated symptoms.

## Usage

1. **Clone this repository** or copy the script into your project.

2. Ensure you have [Python 3.x](https://www.python.org/downloads/) and the following packages installed:

   ```bash
   pip install pandas
   ```

3. **Run the script**:

   ```bash
   python flatten.py
   ```



4. **Result:**
   You’ll get a `flattened_url.csv` file in your working directory.

## Example

**Input disease string:**

```
UMLS:C0376358_malignant neoplasm of prostate^UMLS:C0600139_carcinoma prostate^UMLS:C0600159_carcinoma digitailis
```

**Becomes three rows:**

```
UMLS:C0376358_malignant neoplasm of prostate, symptom_1, symptom_2, ...
UMLS:C0600139_carcinoma prostate, symptom_1, symptom_2, ...
UMLS:C0600159_carcinoma digitailis, symptom_1, symptom_2, ...
```

## Full Script

```python
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
```

### Raw data to flattended data

Before Raw data

<img width="1076" height="234" alt="image" src="https://github.com/user-attachments/assets/ba927d36-f878-47be-9c2e-2882bc5a7152" />

After

Flattened data (Comma separated)

<img width="1796" height="23" alt="image" src="https://github.com/user-attachments/assets/5747fff8-c3e3-411d-8ada-554ac35a8d7e" />


   ```bash
UMLS:C0008031_pain chest,UMLS:C0392680_shortness of breath,UMLS:C0012833_dizziness,UMLS:C0004093_asthenia,UMLS:C0085639_fall,UMLS:C0039070_syncope,UMLS:C0042571_vertigo,UMLS:C0038990_sweat,UMLS:C0700590_sweating increased,UMLS:C0030252_palpitation,UMLS:C0027497_nausea,UMLS:C0002962_angina pectoris,UMLS:C0438716_pressure chest
   ```



## License

MIT


## References
1. https://people.dbmi.columbia.edu/~friedma/Projects/DiseaseSymptomKB/index.html
2. https://github.com/anujdutt9/Disease-Prediction-from-Symptoms
