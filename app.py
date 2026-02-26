import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Trader Sentiment Dashboard", layout="wide")

st.title("📊 Trader Performance vs Market Sentiment")
st.markdown("Exploring how Bitcoin Fear & Greed indices impact trader behavior and profitability.")

# Load the data generated from the Jupyter Notebook
@st.cache_data
def load_data():
    try:
        return pd.read_csv('processed_metrics.csv')
    except FileNotFoundError:
        st.error("Missing 'processed_metrics.csv'. Please run the Jupyter Notebook first!")
        return pd.DataFrame()

df = load_data()

if not df.empty:
    # --- SIDEBAR FILTERS ---
    st.sidebar.header("Filter Data")
    sentiments = st.sidebar.multiselect("Market Sentiment:", options=df['Classification'].unique(), default=df['Classification'].unique())
    trader_types = st.sidebar.multiselect("Trader Segment:", options=df['Trader_Type'].unique(), default=df['Trader_Type'].unique())

    # Apply filters
    filtered_df = df[(df['Classification'].isin(sentiments)) & (df['Trader_Type'].isin(trader_types))]

    # --- KPI METRICS ---
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total PnL (Filtered)", f"${filtered_df['daily_PnL'].sum():,.0f}")
    col2.metric("Avg Daily PnL", f"${filtered_df['daily_PnL'].mean():,.0f}")
    col3.metric("Avg Win Rate", f"{filtered_df['win_rate'].mean() * 100:.1f}%")
    col4.metric("Avg Trades per Day", f"{filtered_df['num_trades'].mean():,.0f}")

    st.markdown("---")

    # --- VISUALIZATIONS ---
    col_chart1, col_chart2 = st.columns(2)

    with col_chart1:
        pnl_agg = filtered_df.groupby('Classification', as_index=False)['daily_PnL'].mean()
        fig_pnl = px.bar(pnl_agg, x='Classification', y='daily_PnL', color='Classification', title="Avg Daily PnL by Sentiment")
        st.plotly_chart(fig_pnl, use_container_width=True)

    with col_chart2:
        freq_agg = filtered_df.groupby(['Classification', 'Trader_Type'], as_index=False)['num_trades'].mean()
        fig_freq = px.bar(freq_agg, x='Classification', y='num_trades', color='Trader_Type', barmode='group', title="Trade Frequency by Segment")
        st.plotly_chart(fig_freq, use_container_width=True)
        