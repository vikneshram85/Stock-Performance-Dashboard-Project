import os
import pandas as pd
import mysql.connector

# MySQL Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stock_data_db"
)

cursor = db.cursor()


csv_folder = r"C:\Users\Nidish Kumaar V\OneDrive\Viknesh\GUVI - Data Science Course Materials\Capstone Projects\Stock Performance Dashboard Project - Updated\csv_by_ticker"

# Loop through all CSV files
for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        filepath = os.path.join(csv_folder, file)

        df = pd.read_csv(filepath)

        # Clean column names
        df.columns = df.columns.str.strip().str.lower()

        # Data cleaning
        df['date'] = pd.to_datetime(df['date'])

        # Insert each row into MySQL
        for _, row in df.iterrows():
            sql = """
            INSERT IGNORE INTO stock_prices
            (ticker, date, open, high, low, close, volume, month)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            data = (
                row['ticker'],
                row['date'],
                float(row['open']),
                float(row['high']),
                float(row['low']),
                float(row['close']),
                int(row['volume']),
                str(row['month'])
            )
            cursor.execute(sql, data)

        print(f"Loaded: {file}")

db.commit()
cursor.close()
db.close()

print("All CSV files imported successfully!")