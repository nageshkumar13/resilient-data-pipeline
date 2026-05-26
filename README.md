# Resilient
Production-style Python ETL pipeline for data validation, cleaning, duplicate detection, reporting, and structured logging
# Resilient Data Pipeline

A Python ETL-style pipeline that processes CSV user data, validates records, separates rejected rows, and generates clean output files.

It is designed for a common data operations problem: inconsistent CSV files that can break reporting, imports, and downstream workflows.

---

# Problem

Businesses often receive CSV files containing:

- invalid email formats
- duplicate records
- missing values
- inconsistent user data

Bad data like this can break downstream systems, analytics, and reporting pipelines.

---

# Solution

This pipeline:

1. Loads raw CSV files
2. Inspects dataset quality
3. Validates email records
4. Detects duplicate rows
5. Separates rejected records
6. Saves clean and rejected outputs separately
7. Generates inspection reports
8. Logs pipeline activity

---

# Project Structure

```text
resilient-data-pipeline/
|
+-- data/
|   +-- raw/
|   +-- processed/
|   +-- rejected/
|
+-- logs/
+-- reports/
|
+-- src/
|   +-- main.py
|   +-- loader.py
|   +-- validator.py
|   +-- cleaner.py
|   +-- logger_config.py
|
+-- requirements.txt
+-- README.md
```

---

# Data Issues Addressed

- Missing email values
- Invalid email formats
- Duplicate user records
- Empty fields
- Dirty CSV input

---

# Output

Running the pipeline generates:

```text
data/processed/processed_users.csv
data/rejected/rejected_users.csv
reports/inspection_report.txt
logs/pipeline.log
```

Rejected rows also include a `rejection_reason` column:

| rejection_reason |
|------------------|
| invalid_email |
| duplicate_row |

The repository includes a sample input file and sample generated outputs so the pipeline can be run and verified immediately.

---

# How to Run

## 1. Create virtual environment

```bash
python -m venv venv
```

## 2. Activate environment

### Windows

```bash
venv\Scripts\activate
```

## 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 4. Run pipeline

After activating the virtual environment, run:

```bash
python src/main.py
```

---

# Potential Enhancements

Possible next improvements:

- Add a few more simple validation rules for required fields
- Allow the input CSV path to be changed without editing code
- Make the text report a little more detailed while keeping the pipeline simple
