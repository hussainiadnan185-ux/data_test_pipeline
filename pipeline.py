import pandas as pd
from pathlib import Path

# ----------------------------
# Paths & Configuration
# ----------------------------

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_DATA_PATH = DATA_DIR / "orders_raw.csv"
CLEAN_DATA_PATH = PROCESSED_DIR / "orders_clean.csv"
QUARANTINE_DATA_PATH = PROCESSED_DIR / "orders_quarantine.csv"

REQUIRED_COLUMNS = [
    "order_id",
    "order_date",
    "product_category",
    "unit_price",
    "quantity",
    "discount"
]

PROCESSED_DIR.mkdir(exist_ok=True)

# ----------------------------
# Load
# ----------------------------

def load_data(path):
    print("Loading data...")
    return pd.read_csv(path)

# ----------------------------
# Cleaning + Quarantine
# ----------------------------

def clean_and_quarantine(df):
    initial_rows = len(df)

    quarantine_conditions = (
        df["order_date"].isna() |
        (df["unit_price"] <= 0) |
        (df["quantity"] <= 0) |
        (~df["discount"].between(0, 0.5))
    )

    quarantine_df = df[quarantine_conditions].copy()
    clean_df = df[~quarantine_conditions].copy()

    # Handle optional fields
    clean_df["product_category"] = clean_df["product_category"].fillna("UNKNOWN")

    # Save outputs
    clean_df.to_csv(CLEAN_DATA_PATH, index=False)
    quarantine_df.to_csv(QUARANTINE_DATA_PATH, index=False)

    print("\n--- CLEANING SUMMARY ---")
    print(f"Rows before processing: {initial_rows}")
    print(f"Clean rows saved:       {len(clean_df)}")
    print(f"Quarantined rows saved: {len(quarantine_df)}")

    return clean_df

# ----------------------------
# Quality Checks
# ----------------------------

def check_schema(df):
    print("Checking schema...")
    missing_cols = set(REQUIRED_COLUMNS) - set(df.columns)
    return list(missing_cols)

def check_missing_values(df):
    print("Checking missing values...")
    return df.isnull().sum()

def check_numeric_ranges(df):
    print("Checking numeric ranges...")
    issues = []

    if (df["unit_price"] <= 0).any():
        issues.append("unit_price has zero or negative values")

    if (df["quantity"] <= 0).any():
        issues.append("quantity has zero or negative values")

    if ((df["discount"] < 0) | (df["discount"] > 0.5)).any():
        issues.append("discount outside allowed range (0–0.5)")

    return issues

# ----------------------------
# Pipeline Runner
# ----------------------------

def run_pipeline():
    df = load_data(RAW_DATA_PATH)

    df_clean = clean_and_quarantine(df)

    schema_issues = check_schema(df_clean)
    missing_values = check_missing_values(df_clean)
    range_issues = check_numeric_ranges(df_clean)

    print("\n--- DATA QUALITY REPORT (CLEAN DATA) ---")

    if schema_issues:
        print("Schema Issues:", schema_issues)
    else:
        print("Schema Check: PASSED")

    print("\nMissing Values by Column:")
    print(missing_values)

    if range_issues:
        print("\nRange Issues:")
        for issue in range_issues:
            print("-", issue)
    else:
        print("\nRange Checks: PASSED")

    if not schema_issues and not range_issues and missing_values.sum() == 0:
        print("\nFINAL STATUS: PASSED")
    else:
        print("\nFINAL STATUS: FAILED")

# ----------------------------
# Entry Point
# ----------------------------

if __name__ == "__main__":
    run_pipeline()
