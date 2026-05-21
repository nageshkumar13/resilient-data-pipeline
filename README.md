# Resilient Data Pipeline

A small Python ETL-style pipeline that processes messy CSV user data, validates records, separates rejected rows, and generates clean output files.

This project simulates a common real-world freelance scenario where businesses receive inconsistent CSV files that break reporting or database workflows.

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
│
├── data/
│   ├── raw/
│   ├── processed/
│   └── rejected/
│
├── logs/
├── reports/
│
├── src/
│   ├── main.py
│   ├── loader.py
│   ├── validator.py
│   ├── cleaner.py
│   └── logger_config.py
│
├── requirements.txt
└── README.md
```

---

# Example Problems Handled

- Missing email values
- Invalid email formats
- Duplicate user records
- Empty fields
- Dirty CSV input

---

# Output

## Processed Data

Clean rows are saved to:

```text
data/processed/processed_users.csv
```

## Rejected Data

Invalid rows are saved to:

```text
data/rejected/rejected_users.csv
```

Rejected rows also include a rejection reason:

| rejection_reason |
|------------------|
| invalid_email |
| duplicate_row |

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

```bash
python src/main.py
```

---

# Skills Demonstrated

- Python automation
- Data validation
- ETL workflow design
- CSV processing
- Error handling
- Modular project structure
- Logging and reporting
- Freelance-style problem solving

---

# Future Improvements

Possible future enhancements:

- PostgreSQL loading
- Scheduled execution
- Email alerts
- Advanced schema validation
- Docker support

This project intentionally keeps Version 1 simple and focused.