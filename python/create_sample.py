
from pathlib import Path
import pandas as pd

# Find the project folder automatically
PROJECT_DIR = Path(__file__).resolve().parent.parent

input_file = PROJECT_DIR / "data" / "raw" / "2019-Oct.csv"
output_file = PROJECT_DIR / "data" / "processed" / "events_sample.csv"

print("Project folder:", PROJECT_DIR)
print("Input file:", input_file)
print("Input file exists:", input_file.exists())
print("Output folder exists:", output_file.parent.exists())

# Columns needed for our project
columns = [
    "event_time",
    "event_type",
    "product_id",
    "category_id",
    "category_code",
    "brand",
    "price",
    "user_id",
    "user_session"
]

# We want data from October 1 and 2
cutoff_date = pd.Timestamp("2019-10-03", tz="UTC")

first_chunk = True
total_rows = 0

# Read the large file in smaller pieces
for chunk in pd.read_csv(
    input_file,
    usecols=columns,
    chunksize=100000
):
    # Convert text dates to datetime values
    chunk["event_time"] = pd.to_datetime(
        chunk["event_time"],
        utc=True,
        errors="coerce"
    )

    # Keep events before October 3
    selected = chunk[
        chunk["event_time"] < cutoff_date
    ]

    # Remove invalid dates and missing session IDs
    selected = selected.dropna(
        subset=["event_time", "user_session"]
    )

    # Save each selected chunk without loading everything into memory
    if not selected.empty:
        selected["event_time"] = selected["event_time"].dt.strftime("%Y-%m-%d %H:%M:%S")
        selected = selected.head(5000)
        selected.to_csv(
            output_file,
            mode="w" if first_chunk else "a",
            header=first_chunk,
            index=False
        )

        first_chunk = False
        total_rows += len(selected)

    print("Rows selected so far:", total_rows)

    # Stop after reaching October 3
    if chunk["event_time"].max() >= cutoff_date:
        break

if total_rows > 0:
    print("\nSample created successfully!")
    print("Total rows:", total_rows)
    print("Saved to:", output_file)
else:
    print("No rows were saved. Check the input file and date range.")
