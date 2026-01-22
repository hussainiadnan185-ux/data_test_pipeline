# Data Quality Pipeline

## Overview
This project implements a **Python-based data quality pipeline**, developed and executed using **VS Code and terminal-based scripts (not Jupyter Notebook)**. The pipeline validates, cleans, and controls raw retail order data before it is used for analytics, dashboards, or AI-driven decision-making.

Instead of silently deleting bad data, the pipeline **quarantines invalid records** and produces clean, auditable datasets suitable for enterprise analytics workflows.

---

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
└── README.md
```

---

## Execution Environment

- **Editor:** Visual Studio Code  
- **Language:** Python  
- **Execution Mode:** Terminal-based script execution  
- **Environment Management:** Python virtual environment (venv)

This project is intentionally implemented as a Python script to ensure **reproducibility, deterministic execution, and production-style behavior**, rather than exploratory notebook execution.

---

## Pipeline Flow

1. Load raw order data from CSV  
2. Apply data cleaning and quarantine rules  
3. Persist clean and quarantined datasets  
4. Run data quality checks on clean data  
5. Report final pipeline status (PASS / FAIL)

---

## Data Quality Rules

### Schema Validation
Mandatory columns:
- `order_id`
- `order_date`
- `product_category`
- `unit_price`
- `quantity`
- `discount`

If any required column is missing, the pipeline fails.

---

### Cleaning & Quarantine Rules

**order_date**
- IF missing → row is quarantined  
- BECAUSE orders without dates cannot be used for time-based analysis

**product_category**
- IF missing → filled with `UNKNOWN`  
- BECAUSE revenue analysis should still include uncategorized orders

**unit_price**
- IF ≤ 0 → row is quarantined  
- BECAUSE zero or negative prices are invalid sales records

**quantity**
- IF ≤ 0 → row is quarantined  
- BECAUSE an order must contain at least one item

**discount**
- IF < 0 or > 0.5 → row is quarantined  
- BECAUSE discounts outside policy indicate invalid or corrupted data

---

## Outputs

### Clean Data
- Path: `data/processed/orders_clean.csv`
- Contains records that satisfy all schema and business rules
- Ready for downstream analytics and reporting

### Quarantined Data
- Path: `data/processed/orders_quarantine.csv`
- Contains records that violate one or more data quality rules
- Preserved for audit and data quality review

---

## Final Status Logic

The pipeline reports **FINAL STATUS: PASSED** only when:
- Schema validation passes
- No missing values remain in clean data
- No numeric range violations remain

Otherwise, it reports **FINAL STATUS: FAILED**.

---

## How to Run

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python pipeline.py
```

---

## Key Design Decisions

- Bad data is **quarantined, not deleted**
- Rules are **explicit and deterministic**
- Outputs are **persisted for traceability**
- Script-based execution mirrors enterprise data pipelines

---

## Limitations

- Quarantined rows do not include per-row failure reasons
- Business rules are hard-coded
- Logging is console-based

---

## Future Improvements

- Add quarantine reason per record
- Externalize rules to configuration
- Add logging and automated tests
- Schedule automated execution

---

## Author

Syed Murtuza Hussaini
