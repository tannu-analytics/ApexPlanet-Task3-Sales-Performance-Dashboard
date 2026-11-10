
import pandas as pd
import os
from io import StringIO

print("======================================")
print("       TASK 3 - DATA INSPECTION")
print("======================================")

file_path = "sales_data.csv"

try:
    df = pd.read_csv(file_path, encoding="utf-8-sig")

    print("\nDataset loaded successfully!")

    print("\n1. DATASET SHAPE")
    print("Rows:", df.shape[0])
    print("Columns:", df.shape[1])

    print("\n2. COLUMN NAMES")
    print(df.columns.tolist())

    print("\n3. FIRST 5 RECORDS")
    print(df.head())

    print("\n4. DATASET INFORMATION")
    df.info()

    print("\n5. MISSING VALUES")
    print(df.isnull().sum())

    print("\n6. DUPLICATE RECORDS")
    print("Duplicates:", df.duplicated().sum())

    print("\n7. STATISTICAL SUMMARY")
    print(df.describe(include="all").to_string())

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/dataset_profile.txt", "w", encoding="utf-8") as f:
        f.write("TASK 3 - DATASET INSPECTION\n")
        f.write("=" * 40 + "\n")
        f.write(f"Total Rows: {df.shape[0]}\n")
        f.write(f"Total Columns: {df.shape[1]}\n\n")
        f.write("COLUMN NAMES:\n")
        f.write(str(df.columns.tolist()) + "\n\n")

        buffer = StringIO()
        df.info(buf=buffer)
        f.write("DATASET INFORMATION:\n")
        f.write(buffer.getvalue() + "\n")

        f.write("MISSING VALUES:\n")
        f.write(df.isnull().sum().to_string() + "\n\n")

        f.write("DUPLICATES:\n")
        f.write(str(df.duplicated().sum()) + "\n\n")

        f.write("STATISTICAL SUMMARY:\n")
        f.write(df.describe(include="all").to_string())

    df.isnull().sum().to_csv("outputs/missing_values.csv")

    print("\nInspection report saved successfully!")
    print("Check the outputs folder.")

except FileNotFoundError:
    print("\nERROR: sales_data.csv file not found!")
    print("Keep the CSV file in the main project folder.")

except Exception as e:
    print("\nAn error occurred:", e)
