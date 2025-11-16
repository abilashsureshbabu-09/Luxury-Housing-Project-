import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path
import os

# Page configuration
st.set_page_config(
    page_title="Luxury Housing Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 Luxury Housing Bangalore Dashboard")
st.markdown("Interactive analytics for luxury housing market in Bangalore")

# Load data
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_data():
    # Support both local and cloud environments
    try:
        # Try relative path first (works in both local and cloud)
        csv_path = Path("data") / "cleaned_luxury_housing.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
        else:
            # Fallback to absolute path from script location
            csv_path = Path(__file__).parent.parent / "data" / "cleaned_luxury_housing.csv"
            df = pd.read_csv(csv_path)
        
        # Convert object columns to string to fix PyArrow serialization
        object_cols = df.select_dtypes(include=['object']).columns
        for col in object_cols:
            df[col] = df[col].astype(str)
        
        return df
    except FileNotFoundError:
        st.error("❌ Data file not found. Ensure 'data/cleaned_luxury_housing.csv' exists.")
        st.stop()

try:
    df = load_data()
    st.success(f"✅ Data loaded successfully! ({len(df):,} records)")
except Exception as e:
    st.error(f"❌ Error loading data: {str(e)}")
    st.stop()

# Sidebar filters
st.sidebar.header("🔍 Filters")

# Get numeric columns for filtering
numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
categorical_cols = df.select_dtypes(include=['object']).columns.tolist()

# Price filter
if 'Price' in numeric_cols or 'price' in df.columns:
    price_col = 'Price' if 'Price' in df.columns else numeric_cols[0]
    price_range = st.sidebar.slider(
        "Price Range",
        min_value=int(df[price_col].min()),
        max_value=int(df[price_col].max()),
        value=(int(df[price_col].min()), int(df[price_col].max()))
    )
    df_filtered = df[(df[price_col] >= price_range[0]) & (df[price_col] <= price_range[1])]
else:
    df_filtered = df

# Key metrics
st.header("📊 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Total Properties", f"{len(df_filtered):,}")

# Calculate numeric statistics
if numeric_cols:
    price_col = numeric_cols[0]
    with col2:
        st.metric("Avg Price", f"₹{df_filtered[price_col].mean():,.0f}")
    with col3:
        st.metric("Median Price", f"₹{df_filtered[price_col].median():,.0f}")
    with col4:
        st.metric("Max Price", f"₹{df_filtered[price_col].max():,.0f}")

# Visualizations
st.header("📈 Visualizations")

# Create tabs for different analyses
tab1, tab2, tab3, tab4 = st.tabs(["Price Distribution", "Data Overview", "Statistics", "Raw Data"])

with tab1:
    if numeric_cols:
        price_col = numeric_cols[0]
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Price Distribution (Histogram)")
            fig_hist = px.histogram(
                df_filtered,
                x=price_col,
                nbins=50,
                title="Distribution of Prices",
                labels={price_col: "Price (₹)"}
            )
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True, key="hist_chart")
        
        with col2:
            st.subheader("Price Box Plot")
            fig_box = go.Figure(data=[go.Box(y=df_filtered[price_col])])
            fig_box.update_layout(
                title="Price Box Plot",
                yaxis_title="Price (₹)",
                height=400
            )
            st.plotly_chart(fig_box, use_container_width=True, key="box_chart")

with tab2:
    st.subheader("Dataset Overview")
    st.write(f"**Dataset Shape:** {df_filtered.shape[0]} rows × {df_filtered.shape[1]} columns")
    st.write(f"**Memory Usage:** {df_filtered.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("**Column Types:**")
        dtypes_df = pd.DataFrame(df_filtered.dtypes.astype(str), columns=['Data Type'])
        st.dataframe(dtypes_df, use_container_width=True)
    with col2:
        st.write("**Missing Values:**")
        missing = df_filtered.isnull().sum()
        if missing.sum() > 0:
            missing_df = pd.DataFrame(missing[missing > 0], columns=['Missing Count'])
            st.dataframe(missing_df, use_container_width=True)
        else:
            st.info("✅ No missing values found!")

with tab3:
    st.subheader("Statistical Summary")
    st.dataframe(df_filtered.describe(), use_container_width=True, key="stats_table")

with tab4:
    st.subheader("Raw Data")
    st.dataframe(df_filtered, use_container_width=True, key="data_table")

# Footer
st.markdown("---")
st.markdown("📍 Luxury Housing Bangalore | Data Dashboard | Last Updated: 2025")
