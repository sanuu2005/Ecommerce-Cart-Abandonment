
import pandas as pd
import oracledb
from pathlib import Path

# Find the CSV file
project_dir = Path(__file__).resolve().parent.parent
file_path = project_dir / "data" / "processed" / "events_sample.csv"

# Oracle login
username = "SYSTEM"
password = input("Enter your Oracle password: ")

connection = oracledb.connect(
    user=username,
    password=password,
    dsn="localhost:1522/freepdb1"
)

cursor = connection.cursor()

insert_sql = """
    INSERT INTO ECOMMERCE_EVENTS (
        EVENT_TIME, EVENT_TYPE, PRODUCT_ID, CATEGORY_ID,
        CATEGORY_CODE, BRAND, PRICE, USER_ID, USER_SESSION
    )
    VALUES (
        :1, :2, :3, :4, :5, :6, :7, :8, :9
    )
"""

total_inserted = 0

try:
    for df in pd.read_csv(
        file_path,
        chunksize=1000,
        dtype={
            "product_id": "string",
            "category_id": "string",
            "user_id": "string"
        }
    ):
        records = []

        for _, row in df.iterrows():
            event_time = pd.to_datetime(
                row["event_time"], utc=True
            ).to_pydatetime()

            def clean(value):
                return None if pd.isna(value) or value == "" else value

            records.append((
                event_time,
                clean(row["event_type"]),
                int(row["product_id"]) if clean(row["product_id"]) is not None else None,
                int(row["category_id"]) if clean(row["category_id"]) is not None else None,
                clean(row["category_code"]),
                clean(row["brand"]),
                float(row["price"]) if clean(row["price"]) is not None else None,
                int(row["user_id"]) if clean(row["user_id"]) is not None else None,
                clean(row["user_session"])
            ))

        if records:
            cursor.executemany(insert_sql, records)
            total_inserted += len(records)
            print("Rows processed:", total_inserted)

    connection.commit()
    print("Data imported successfully!")
    print("Total rows inserted:", total_inserted)

except Exception as error:
    connection.rollback()
    print("Import failed:", error)

finally:
    cursor.close()
    connection.close()

