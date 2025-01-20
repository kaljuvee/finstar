import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta

# Set page configuration
st.set_page_config(
    page_title="Portfolio Asset Management",
    page_icon="📊",
    layout="wide"
)

# Initialize Faker
fake = Faker()

# Generate fake portfolio data
def generate_portfolio_data(num_assets=5):
    assets = ['Stock', 'Bond', 'Real Estate', 'Cryptocurrency', 'Commodities']
    colors = px.colors.qualitative.Set3[:num_assets]
    
    portfolio_data = {
        'Asset': assets[:num_assets],
        'Value': [round(fake.random.uniform(10000, 100000), 2) for _ in range(num_assets)],
        'Returns': [round(fake.random.uniform(-15, 25), 2) for _ in range(num_assets)],
        'Risk': [round(fake.random.uniform(5, 20), 2) for _ in range(num_assets)],
        'Colors': colors
    }
    return pd.DataFrame(portfolio_data)

# Generate historical data
def generate_historical_data(days=30):
    dates = [(datetime.now() - timedelta(days=x)).date() for x in range(days)]
    portfolio_values = []
    initial_value = 100000
    
    for i in range(days):
        daily_change = fake.random.uniform(-0.02, 0.02)
        initial_value *= (1 + daily_change)
        portfolio_values.append(round(initial_value, 2))
    
    return pd.DataFrame({
        'Date': dates,
        'Portfolio Value': portfolio_values
    })

# Main dashboard
st.title("Portfolio Asset Management Dashboard")

# Generate data
if 'portfolio_df' not in st.session_state:
    st.session_state.portfolio_df = generate_portfolio_data()
if 'historical_df' not in st.session_state:
    st.session_state.historical_df = generate_historical_data()

# Refresh Data Button
if st.button("Refresh Data"):
    st.session_state.portfolio_df = generate_portfolio_data()
    st.session_state.historical_df = generate_historical_data()

# Portfolio Overview Section
if st.button("Show Portfolio Overview"):
    st.header("Portfolio Overview")
    
    # Show raw data first
    st.subheader("Raw Portfolio Data")
    st.dataframe(st.session_state.portfolio_df.drop('Colors', axis=1), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    total_value = st.session_state.portfolio_df['Value'].sum()
    avg_return = st.session_state.portfolio_df['Returns'].mean()
    avg_risk = st.session_state.portfolio_df['Risk'].mean()
    
    col1.metric("Total Portfolio Value", f"${total_value:,.2f}")
    col2.metric("Average Return", f"{avg_return:.2f}%")
    col3.metric("Average Risk", f"{avg_risk:.2f}%")

# Asset Allocation Section
if st.button("Show Asset Allocation"):
    st.header("Asset Allocation Analysis")
    
    # Show allocation data
    st.subheader("Asset Allocation Data")
    allocation_data = st.session_state.portfolio_df[['Asset', 'Value']].copy()
    allocation_data['Percentage'] = (allocation_data['Value'] / allocation_data['Value'].sum() * 100).round(2)
    st.dataframe(allocation_data.style.format({
        'Value': '${:,.2f}',
        'Percentage': '{:.2f}%'
    }), use_container_width=True)
    
    # Show pie chart
    fig_pie = px.pie(
        st.session_state.portfolio_df,
        values='Value',
        names='Asset',
        color='Asset',
        color_discrete_sequence=st.session_state.portfolio_df['Colors'],
        title='Asset Allocation Distribution'
    )
    st.plotly_chart(fig_pie, use_container_width=True)

# Historical Performance Section
if st.button("Show Historical Performance"):
    st.header("Historical Performance Analysis")
    
    # Show historical data
    st.subheader("Historical Data")
    st.dataframe(st.session_state.historical_df.style.format({
        'Portfolio Value': '${:,.2f}'
    }), use_container_width=True)
    
    # Show line chart
    fig_line = px.line(
        st.session_state.historical_df,
        x='Date',
        y='Portfolio Value',
        title='Historical Portfolio Value'
    )
    fig_line.update_traces(line_color='#2E86C1')
    st.plotly_chart(fig_line, use_container_width=True)

# Risk vs Return Section
if st.button("Show Risk vs Return Analysis"):
    st.header("Risk vs Return Analysis")
    
    # Show risk-return data
    st.subheader("Risk-Return Data")
    risk_return_data = st.session_state.portfolio_df[['Asset', 'Risk', 'Returns', 'Value']].copy()
    st.dataframe(risk_return_data.style.format({
        'Value': '${:,.2f}',
        'Returns': '{:.2f}%',
        'Risk': '{:.2f}%'
    }), use_container_width=True)
    
    # Show scatter plot
    fig_scatter = px.scatter(
        st.session_state.portfolio_df,
        x='Risk',
        y='Returns',
        size='Value',
        color='Asset',
        color_discrete_sequence=st.session_state.portfolio_df['Colors'],
        title='Risk vs Return by Asset',
        labels={'Risk': 'Risk (%)', 'Returns': 'Return (%)'}
    )
    st.plotly_chart(fig_scatter, use_container_width=True)

# Detailed Asset Analysis
if st.button("Show Detailed Asset Analysis"):
    st.header("Detailed Asset Analysis")
    
    # Show formatted table
    st.subheader("Complete Asset Details")
    styled_df = st.session_state.portfolio_df.drop('Colors', axis=1).style.format({
        'Value': '${:,.2f}',
        'Returns': '{:.2f}%',
        'Risk': '{:.2f}%'
    })
    st.dataframe(styled_df, use_container_width=True)
    
    # Add summary statistics
    st.subheader("Summary Statistics")
    summary_stats = st.session_state.portfolio_df[['Value', 'Returns', 'Risk']].describe()
    st.dataframe(summary_stats.style.format({
        'Value': '${:,.2f}',
        'Returns': '{:.2f}',
        'Risk': '{:.2f}'
    }), use_container_width=True)

# Footer
st.markdown("---")
st.markdown("*Note: This is a demo dashboard with randomly generated data. Click 'Refresh Data' to generate new random data.*") 