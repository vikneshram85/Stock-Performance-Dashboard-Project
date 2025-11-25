import streamlit as st
import pandas as pd
import mysql.connector

# ------------------------------------------------
# Load Data from MySQL (cached for performance)
# ------------------------------------------------
@st.cache_data
def load_data():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="stocks_db"
    )
    df = pd.read_sql("SELECT * FROM stock_summary", conn)
    conn.close()
    return df


# ----------------------------------------
# Streamlit Page Settings
# ----------------------------------------
st.set_page_config(page_title="Stock Summary Dashboard", layout="wide")

st.title("📊 Stock Market Summary Dashboard")
st.write("Dashboard generated from MySQL `stock_summary` table.")


# ----------------------------------------
# Load Data
# ----------------------------------------
df = load_data()


# ----------------------------------------
# Metrics Calculations
# ----------------------------------------
top_10_green = df.sort_values(by="yearly_return", ascending=False).head(10)
top_10_loss = df.sort_values(by="yearly_return", ascending=True).head(10)

green_count = (df["yearly_return"] > 0).sum()
red_count = (df["yearly_return"] < 0).sum()

average_price = df["avg_close"].mean()
average_volume = df["avg_volume"].mean()


# ----------------------------------------
# Show Metrics
# ----------------------------------------
st.header("📈 Market Summary Metrics")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Green Stocks", green_count)
col2.metric("Red Stocks", red_count)
col3.metric("Average Price", round(average_price, 2))
col4.metric("Average Volume", round(average_volume, 2))


# ----------------------------------------
# Top Stocks Section
# ----------------------------------------
st.header("🏆 Top 10 Green Stocks (Best Performers)")
st.dataframe(top_10_green)

st.header("📉 Top 10 Loss Stocks (Worst Performers)")
st.dataframe(top_10_loss)


# ----------------------------------------
# Interactive Ticker Selection
# ----------------------------------------
st.header("🔍 Explore Stock Details")

unique_tickers = df["Ticker"].unique()
selected_ticker = st.selectbox("Select a Ticker to Explore:", unique_tickers)

st.subheader(f"📌 Details for: {selected_ticker}")
st.dataframe(df[df["Ticker"] == selected_ticker])


# ----------------------------------------
# Chart Section
# ----------------------------------------
st.header("📊 Yearly Return Bar Chart")
st.bar_chart(df.set_index("Ticker")["yearly_return"])
