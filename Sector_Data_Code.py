import pandas as pd
import mysql.connector

# ---------------------------------------
# 1. LOAD CSV
# ---------------------------------------
df = pd.read_csv(r"C:\Users\Nidish Kumaar V\OneDrive\Viknesh\GUVI - Data Science Course Materials\Capstone Projects\Stock Performance Dashboard Project - Updated\Sector_data - Sheet1.csv")

# Strip quotes and spaces from column names
df.columns = df.columns.str.strip().str.replace('"', '').str.upper()

# Strip spaces and clean values
df["COMPANY"] = df["COMPANY"].astype(str).str.strip().str.replace('"', '')
df["SECTOR"] = df["SECTOR"].astype(str).str.strip().str.replace('"', '')
df["SYMBOL"] = df["SYMBOL"].astype(str).str.strip().str.replace('"', '').str.upper()

print("Preview:\n", df.head())

# ---------------------------------------
# 2. CONNECT TO MYSQL
# ---------------------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stock_data_db"
)

cursor = conn.cursor()

# ---------------------------------------
# 3. CREATE TABLE IF NOT EXISTS
# ---------------------------------------
create_table = """
CREATE TABLE IF NOT EXISTS sector_data (
    COMPANY VARCHAR(255),
    SECTOR VARCHAR(255),
    SYMBOL VARCHAR(255)
);
"""
cursor.execute(create_table)

# ---------------------------------------
# 4. INSERT DATA
# ---------------------------------------
insert_query = """
INSERT INTO sector_data (COMPANY, SECTOR, SYMBOL)
VALUES (%s, %s, %s)
"""

for _, row in df.iterrows():
    cursor.execute(insert_query, (row["COMPANY"], row["SECTOR"], row["SYMBOL"]))

conn.commit()
cursor.close()
conn.close()

print("sector_data uploaded successfully!")
