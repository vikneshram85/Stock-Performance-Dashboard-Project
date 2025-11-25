import os
import mysql.connector

csv_folder = r"C:\Users\Nidish Kumaar V\OneDrive\Viknesh\GUVI - Data Science Course Materials\Capstone Projects\Stock Performance Dashboard Project\csv_output"

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stocks_db",
    allow_local_infile=True
)
cursor = conn.cursor()

for file in os.listdir(csv_folder):
    if file.endswith(".csv"):
        full_path = os.path.join(csv_folder, file)
        print("Loading:", file)

        query = f"""
        LOAD DATA LOCAL INFILE '{full_path.replace('\\','/')}'
        INTO TABLE master_stock_data
        FIELDS TERMINATED BY ','
        ENCLOSED BY '"'
        IGNORE 1 LINES;
        """

        cursor.execute(query)
        conn.commit()

cursor.close()
conn.close()
