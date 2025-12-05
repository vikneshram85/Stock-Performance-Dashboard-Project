import streamlit as st
import pandas as pd
import mysql.connector

# --- MySQL Connection ---
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="stock_data_db"
)

# Read all data into a DataFrame
query = "SELECT * FROM stock_prices;"
df = pd.read_sql(query, db)

db.close()

# --- Preprocessing ---
# Convert date column to datetime
df['date'] = pd.to_datetime(df['date'])

# Calculate yearly return per ticker
# Yearly Return = (Last Close of Year - First Close of Year) / First Close
def calculate_yearly_return(df, year):
    df_year = df[df['date'].dt.year == year]
    returns = []
    for ticker, group in df_year.groupby('ticker'):
        first_close = group.sort_values('date')['close'].iloc[0]
        last_close = group.sort_values('date')['close'].iloc[-1]
        yearly_return = (last_close - first_close) / first_close * 100
        returns.append({'ticker': ticker, 'yearly_return': yearly_return})
    return pd.DataFrame(returns)

current_year = df['date'].dt.year.max()
returns_df = calculate_yearly_return(df, current_year)

# --- Top 10 Green & Loss Stocks ---
top_10_green = returns_df.sort_values('yearly_return', ascending=False).head(10)
top_10_loss = returns_df.sort_values('yearly_return', ascending=True).head(10)

# --- Market Summary ---
latest_prices = df.sort_values('date').groupby('ticker').tail(1)
green_count = (latest_prices['close'] >= latest_prices['open']).sum()
red_count = (latest_prices['close'] < latest_prices['open']).sum()
avg_price = latest_prices['close'].mean()
avg_volume = latest_prices['volume'].mean()

# --- Streamlit Dashboard ---
st.title("Stock Market Key Metrics")

st.subheader(f"Top 10 Green Stocks ({current_year})")
st.dataframe(top_10_green)

st.subheader(f"Top 10 Loss Stocks ({current_year})")
st.dataframe(top_10_loss)

st.subheader("Market Summary")
st.write(f"Green Stocks: {green_count}")
st.write(f"Red Stocks: {red_count}")
st.write(f"Average Price: {avg_price:.2f}")
st.write(f"Average Volume: {avg_volume:.0f}")
