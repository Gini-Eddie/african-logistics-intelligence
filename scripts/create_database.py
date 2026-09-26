from pathlib import Path
import sqlite3
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent

DATA_DIR = BASE_DIR / "data" / "scenario"
DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(parents=True, exist_ok=True)

DATABASE_PATH = DATABASE_DIR / "logistics_v1.db"


# Connect to SQLite
connection = sqlite3.connect(DATABASE_PATH)


# =========================================================
# LOAD CSV FILES
# =========================================================

tables = {
    "depots": "depot.csv",
    "riders": "riders.csv",
    "deliveries": "deliveries.csv",
    "scenarios": "scenario.csv"
}


for table_name, filename in tables.items():

    file_path = DATA_DIR / filename

    dataframe = pd.read_csv(file_path)

    dataframe.to_sql(
        table_name,
        connection,
        if_exists="replace",
        index=False
    )

    print(
        f"{table_name}: "
        f"{len(dataframe)} records loaded."
    )


connection.close()

print("\nSQLite database created:")
print(DATABASE_PATH)