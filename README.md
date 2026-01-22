Data Quality Pipeline
Overview

This project implements a Python-based data quality pipeline built and executed using VS Code and the terminal (not Jupyter Notebook). The pipeline validates, cleans, and controls raw order data before it is used for analytics or reporting.

Instead of silently deleting bad data, the pipeline separates clean and invalid records, making the process auditable and production-oriented.
## Project Structure

```text
data_quality_pipeline/
│
├── data/
│   ├── orders_raw.csv
│   └── processed/
│       ├── orders_clean.csv
│       └── orders_quarantine.csv
│
├── pipeline.py
├── requirements.txt
├── README.md

```

Execution Environment

Editor: Visual Studio Code

Language: Python

Execution: Terminal-based script execution

Environment: Python virtual environment (venv)

This project was intentionally implemented as a Python script rather than a Jupyter notebook to ensure reproducibility and production-style execution.

Pipeline Flow

Load raw order data from CSV

Apply cleaning and quarantine rules

Persist clean and quarantined datasets

Run data quality checks on clean data

Report final pipeline status (PASS / FAIL)

Data Quality Rules
1. Schema Validation

The following columns are mandatory:

order_id

order_date

product_category

unit_price

quantity

discount

If any required column is missing, the pipeline fails.

2. Cleaning & Quarantine Rules

The pipeline enforces explicit business rules:

order_date

IF order_date is missing

THEN row is quarantined

BECAUSE orders without dates cannot be used for time-based analysis

product_category

IF product_category is missing

THEN fill with UNKNOWN

BECAUSE revenue should still be counted even when category data is unavailable

unit_price

IF unit_price ≤ 0

THEN row is quarantined

BECAUSE zero or negative prices are invalid sales records

quantity

IF quantity ≤ 0

THEN row is quarantined

BECAUSE an order must contain at least one item

discount

IF discount < 0 OR discount > 0.5

THEN row is quarantined

BECAUSE discounts outside policy indicate corrupted or invalid data

Outputs
Clean Data

Path: data/processed/orders_clean.csv

Contains records that satisfy all schema and business rules

Ready for downstream analytics and reporting

Quarantined Data

Path: data/processed/orders_quarantine.csv

Contains records that violate one or more data quality rules

Preserved for audit and data quality review

Final Status Logic

The pipeline reports FINAL STATUS: PASSED only when:

Schema validation passes

No missing values remain in clean data

No numeric range violations remain

Otherwise, the pipeline reports FINAL STATUS: FAILED.

How to Run

From the project root with the virtual environment activated:

python pipeline.py
Key Design Decisions

Bad data is quarantined, not deleted

Rules are explicit and consistently enforced

Outputs are persisted for traceability

Script-based execution ensures reproducibility

Limitations

Quarantined rows do not yet include per-row failure reasons

Business rules are currently hard-coded

Logging uses console output instead of a logging framework

Future Improvements

Add quarantine reason per record

Externalize rules to configuration files

Add logging and automated tests

Schedule pipeline execution
