

import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stocks_db"
)

# Load stock_summary table
df = pd.read_sql("SELECT * FROM stock_summary", conn)
conn.close()

df.head()

top_10_green = df.sort_values(by="yearly_return", ascending=False).head(10)
print(top_10_green)

top_10_loss = df.sort_values(by="yearly_return").head(10)
print(top_10_loss)

green_count = (df["yearly_return"] > 0).sum()
red_count = (df["yearly_return"] < 0).sum()

print("Green stocks:", green_count)
print("Red stocks:", red_count)

average_price = df["avg_close"].mean()
print("Average price across all stocks:", average_price)


average_volume = df["avg_volume"].mean()
print("Average volume across all stocks:", average_volume)


import pandas as pd
import mysql.connector

# Connect to MySQL
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stocks_db"
)

# Load stock_summary table
df = pd.read_sql("SELECT * FROM stock_summary", conn)
conn.close()

# Top 10 Green
top_10_green = df.sort_values(by="yearly_return", ascending=False).head(10)

# Top 10 Loss
top_10_loss = df.sort_values(by="yearly_return").head(10)

# Market Summary
green_count = (df["yearly_return"] > 0).sum()
red_count = (df["yearly_return"] < 0).sum()

average_price = df["avg_close"].mean()
average_volume = df["avg_volume"].mean()

print("Top 10 Green Stocks:")
print(top_10_green)

print("\nTop 10 Loss Stocks:")
print(top_10_loss)

print("\nMarket Summary:")
print("Green stocks:", green_count)
print("Red stocks:", red_count)
print("Average Price:", average_price)
print("Average Volume:", average_volume)


