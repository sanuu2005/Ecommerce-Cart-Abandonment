
import pandas as pd
from pathlib import Path

# Locate the sample file
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "processed" / "events_sample.csv"

print("File exists:", file_path.exists())

if file_path.exists():
    df = pd.read_csv(file_path)

    print("\nNumber of rows:", len(df))
    print("\nColumn names:")
    print(df.columns.tolist())

    print("\nFirst 5 rows:")
    print(df.head())

    print("\nEvent type counts:")
    print(df["event_type"].value_counts(dropna=False))

    print("\nMissing values:")
    print(df.isnull().sum())
else:
    print("Sample file not found. Check the file path.")
