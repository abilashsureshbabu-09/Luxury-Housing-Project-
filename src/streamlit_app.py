import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from pathlib import Path

# Page configuration
st.set_page_config(
    page_title="Luxury Housing Dashboard",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Title and description
st.title("🏠 Luxury Housing Bangalore Dashboard")
st.markdown("### Interactive Analytics for Luxury Housing Market in Bangalore")
st.markdown("Comprehensive analysis of property prices, market trends, and buyer insights")

# Load data
@st.cache_data(ttl=3600)
def load_data():
    try:
        csv_path = Path("data") / "cleaned_luxury_housing.csv"
        if csv_path.exists():
            df = pd.read_csv(csv_path)
        else:
            csv_path = Path(__file__).parent.parent / "data" / "cleaned_luxury_housing.csv"
            df = pd.read_csv(csv_path)
        
        # Convert object columns to string
        object_cols = df.select_dtypes(include=['object']).columns
        for col in object_cols:
            df[col] = df[col].astype(str)
        
        # Clean data: Remove rows with invalid prices (negative or zero)
        df = df[df['ticket_price_inr'] > 0].copy()
        df = df[df['ticket_price_cr'] > 0].copy()
        
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
st.sidebar.header("🔍 Advanced Filters")

# Price filter
price_min = int(df['ticket_price_inr'].min())
price_max = int(df['ticket_price_inr'].max())
price_range = st.sidebar.slider(
    "Price Range (₹)",
    min_value=price_min,
    max_value=price_max,
    value=(price_min, price_max),
    step=int((price_max - price_min) / 100) if (price_max - price_min) > 100 else 1
)

# Configuration filter
configurations = df['configuration'].unique().tolist()
selected_config = st.sidebar.multiselect(
    "Select Configuration",
    configurations,
    default=configurations[:5] if len(configurations) > 5 else configurations
)

# Buyer type filter
buyer_types = df['buyer_type'].unique().tolist()
selected_buyer_type = st.sidebar.multiselect(
    "Select Buyer Type",
    buyer_types,
    default=buyer_types
)

# Micro market filter
micro_markets = sorted(df['micro_market'].unique().tolist())
selected_markets = st.sidebar.multiselect(
    "Select Micro Markets",
    micro_markets,
    default=micro_markets[:10] if len(micro_markets) > 10 else micro_markets
)

# Apply filters
df_filtered = df[
    (df['ticket_price_inr'] >= price_range[0]) & 
    (df['ticket_price_inr'] <= price_range[1]) &
    (df['configuration'].isin(selected_config)) &
    (df['buyer_type'].isin(selected_buyer_type)) &
    (df['micro_market'].isin(selected_markets))
]

# Key metrics section
st.header("📊 Key Metrics")
col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Total Properties", f"{len(df_filtered):,}")
with col2:
    st.metric("Avg Price (₹Cr)", f"{df_filtered['ticket_price_cr'].mean():.2f}")
with col3:
    st.metric("Median Price (₹Cr)", f"{df_filtered['ticket_price_cr'].median():.2f}")
with col4:
    st.metric("Avg Size (sqft)", f"{df_filtered['unit_size_sqft'].mean():,.0f}")
with col5:
    st.metric("Avg Connectivity", f"{df_filtered['connectivity_score'].mean():.2f}")

# Main visualizations
st.header("📈 Market Analysis")

# Row 1: Price Distribution and Price vs Size
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Distribution")
    fig_hist = px.histogram(
        df_filtered,
        x='ticket_price_cr',
        nbins=50,
        title="Distribution of Property Prices",
        labels={'ticket_price_cr': 'Price (₹ Crores)'},
        color_discrete_sequence=['#1f77b4']
    )
    fig_hist.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_hist, use_container_width=True)

with col2:
    st.subheader("Price vs Property Size")
    fig_scatter = px.scatter(
        df_filtered,
        x='unit_size_sqft',
        y='ticket_price_cr',
        color='connectivity_score',
        size='bedrooms',
        hover_data=['project_name', 'micro_market'],
        title="Property Price vs Size",
        labels={'unit_size_sqft': 'Size (sqft)', 'ticket_price_cr': 'Price (₹ Cr)', 'connectivity_score': 'Connectivity'}
    )
    fig_scatter.update_layout(height=400)
    st.plotly_chart(fig_scatter, use_container_width=True)

# Row 2: Top Markets and Configuration Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Top 10 Micro Markets by Average Price")
    top_markets = df_filtered.groupby('micro_market')['ticket_price_cr'].mean().nlargest(10).reset_index()
    fig_bar = px.bar(
        top_markets,
        x='ticket_price_cr',
        y='micro_market',
        orientation='h',
        title="Average Price by Micro Market",
        labels={'ticket_price_cr': 'Avg Price (₹ Cr)', 'micro_market': 'Micro Market'},
        color='ticket_price_cr',
        color_continuous_scale='Viridis'
    )
    fig_bar.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_bar, use_container_width=True)

with col2:
    st.subheader("Configuration Distribution")
    config_dist = df_filtered['configuration'].value_counts().head(10)
    fig_pie = px.pie(
        names=config_dist.index,
        values=config_dist.values,
        title="Top 10 Configuration Types",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_layout(height=400)
    st.plotly_chart(fig_pie, use_container_width=True)

# Row 3: Connectivity vs Amenity and Buyer Type Analysis
col1, col2 = st.columns(2)

with col1:
    st.subheader("Connectivity vs Amenity Scores")
    # Filter out rows with missing or invalid data
    df_bubble = df_filtered.dropna(subset=['amenity_score', 'connectivity_score', 'ticket_price_cr'])
    # Remove invalid prices (negative or zero)
    df_bubble = df_bubble[(df_bubble['ticket_price_cr'] > 0) & (df_bubble['connectivity_score'] > 0) & (df_bubble['amenity_score'] > 0)]
    
    if len(df_bubble) > 10:
        try:
            fig_bubble = px.scatter(
                df_bubble,
                x='connectivity_score',
                y='amenity_score',
                size='ticket_price_cr',
                color='ticket_price_cr',
                hover_data=['micro_market', 'project_name'],
                title="Infrastructure Scores Impact",
                labels={'connectivity_score': 'Connectivity Score', 'amenity_score': 'Amenity Score'},
                color_continuous_scale='Portland'
            )
            fig_bubble.update_layout(height=400)
            st.plotly_chart(fig_bubble, use_container_width=True)
        except Exception as e:
            st.error(f"Error creating chart: {str(e)}")
    else:
        st.info("ℹ️ Not enough data with valid amenity scores for current filters")

with col2:
    st.subheader("Buyer Type Analysis")
    buyer_analysis = df_filtered.groupby('buyer_type').agg({
        'ticket_price_cr': ['mean', 'count']
    }).reset_index()
    buyer_analysis.columns = ['Buyer Type', 'Avg Price', 'Count']
    
    fig_buyer = go.Figure(data=[
        go.Bar(name='Count', x=buyer_analysis['Buyer Type'], y=buyer_analysis['Count'], yaxis='y', marker_color='lightblue'),
        go.Bar(name='Avg Price (₹Cr)', x=buyer_analysis['Buyer Type'], y=buyer_analysis['Avg Price'], yaxis='y2', marker_color='orange')
    ])
    fig_buyer.update_layout(
        title='Buyer Type: Count and Average Price',
        yaxis=dict(title='Count'),
        yaxis2=dict(title='Avg Price (₹Cr)', overlaying='y', side='right'),
        hovermode='x unified',
        height=400
    )
    st.plotly_chart(fig_buyer, use_container_width=True)

# Row 4: Possession Status and Transaction Type
col1, col2 = st.columns(2)

with col1:
    st.subheader("Possession Status")
    possession_data = df_filtered['possession_status'].value_counts()
    fig_poss = px.bar(
        x=possession_data.index,
        y=possession_data.values,
        title="Properties by Possession Status",
        labels={'x': 'Status', 'y': 'Count'},
        color=possession_data.values,
        color_continuous_scale='Reds'
    )
    fig_poss.update_layout(height=400, showlegend=False)
    st.plotly_chart(fig_poss, use_container_width=True)

with col2:
    st.subheader("Transaction Type Distribution")
    trans_data = df_filtered['transaction_type'].value_counts()
    fig_trans = px.donut(
        names=trans_data.index,
        values=trans_data.values,
        title="Transaction Types",
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    fig_trans.update_layout(height=400)
    st.plotly_chart(fig_trans, use_container_width=True)

# Row 5: Bedroom Distribution and NRI Buyers
col1, col2 = st.columns(2)

with col1:
    st.subheader("Bedrooms vs Average Price")
    bedroom_price = df_filtered.groupby('bedrooms')['ticket_price_cr'].agg(['mean', 'count']).reset_index()
    bedroom_price = bedroom_price[bedroom_price['count'] > 10].sort_values('bedrooms')
    
    if len(bedroom_price) > 0:
        fig_bed = go.Figure()
        fig_bed.add_trace(go.Bar(
            x=bedroom_price['bedrooms'],
            y=bedroom_price['mean'],
            marker_color='steelblue',
            name='Avg Price'
        ))
        fig_bed.update_layout(
            title='Average Price by Bedroom Count',
            xaxis_title='Bedrooms',
            yaxis_title='Avg Price (₹ Cr)',
            height=400,
            showlegend=False
        )
        st.plotly_chart(fig_bed, use_container_width=True)
    else:
        st.info("ℹ️ No bedroom data available for current filters")

with col2:
    st.subheader("NRI Buyer Percentage")
    nri_data = df_filtered['nri_buyer'].value_counts()
    
    if len(nri_data) > 0:
        nri_yes = nri_data.get('Yes', 0)
        nri_no = nri_data.get('No', 0)
        nri_pct = (nri_yes / (nri_yes + nri_no) * 100) if (nri_yes + nri_no) > 0 else 0
        
        fig_nri = go.Figure(data=[
            go.Pie(
                labels=['NRI Buyers', 'Local Buyers'],
                values=[nri_pct, 100 - nri_pct],
                marker_colors=['#FF6B6B', '#4ECDC4'],
                hole=0.4
            )
        ])
        fig_nri.update_layout(title=f"NRI Buyer Distribution ({nri_pct:.1f}% NRI)", height=400)
        st.plotly_chart(fig_nri, use_container_width=True)
    else:
        st.info("ℹ️ No NRI buyer data available for current filters")

# Row 6: Market Trends by Quarter
col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Trends by Quarter")
    quarterly = df_filtered.groupby('fiscal_quarter')['ticket_price_cr'].agg(['mean', 'count']).reset_index()
    quarterly = quarterly.sort_values('fiscal_quarter')
    
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Scatter(
        x=quarterly['fiscal_quarter'],
        y=quarterly['mean'],
        mode='lines+markers',
        name='Avg Price',
        line=dict(color='#FF6B6B', width=3),
        marker=dict(size=10)
    ))
    fig_trend.update_layout(
        title='Average Price Trend Over Time',
        xaxis_title='Quarter',
        yaxis_title='Avg Price (₹ Cr)',
        height=400,
        hovermode='x unified'
    )
    st.plotly_chart(fig_trend, use_container_width=True)

with col2:
    st.subheader("Sales Channel Performance")
    channel_data = df_filtered.groupby('sales_channel').agg({
        'ticket_price_cr': 'mean',
        'property_id': 'count'
    }).reset_index()
    channel_data.columns = ['Sales Channel', 'Avg Price', 'Count']
    
    fig_channel = px.bar(
        channel_data,
        x='Sales Channel',
        y='Avg Price',
        color='Count',
        title="Sales Channel Analysis",
        labels={'Avg Price': 'Avg Price (₹ Cr)', 'Count': 'Number of Properties'},
        color_continuous_scale='Teal'
    )
    fig_channel.update_layout(height=400)
    st.plotly_chart(fig_channel, use_container_width=True)

# Data insights section
st.header("📋 Detailed Data Tables")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Raw Data", 
    "Summary Statistics", 
    "Market Comparison", 
    "Developer Performance",
    "Data Info"
])

with tab1:
    st.subheader("Full Dataset")
    st.dataframe(df_filtered, use_container_width=True, key="full_data")

with tab2:
    st.subheader("Statistical Summary")
    st.dataframe(df_filtered.describe(), use_container_width=True, key="stats_summary")

with tab3:
    st.subheader("Market Comparison by Micro Market")
    market_comp = df_filtered.groupby('micro_market').agg({
        'ticket_price_cr': ['count', 'mean', 'median', 'min', 'max'],
        'unit_size_sqft': 'mean',
        'connectivity_score': 'mean'
    }).round(2)
    market_comp.columns = ['Count', 'Avg Price', 'Median Price', 'Min Price', 'Max Price', 'Avg Size', 'Connectivity']
    market_comp = market_comp.sort_values('Avg Price', ascending=False)
    st.dataframe(market_comp, use_container_width=True)

with tab4:
    st.subheader("Developer Performance")
    dev_perf = df_filtered.groupby('developer_name').agg({
        'property_id': 'count',
        'ticket_price_cr': ['mean', 'median'],
        'connectivity_score': 'mean',
        'amenity_score': 'mean'
    }).round(2)
    dev_perf.columns = ['Projects', 'Avg Price', 'Median Price', 'Connectivity', 'Amenity']
    dev_perf = dev_perf.sort_values('Projects', ascending=False).head(20)
    st.dataframe(dev_perf, use_container_width=True)

with tab5:
    st.subheader("Dataset Information")
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

# Download section
st.header("📥 Download Data")
csv = df_filtered.to_csv(index=False)
st.download_button(
    label="Download Filtered Data (CSV)",
    data=csv,
    file_name="luxury_housing_filtered.csv",
    mime="text/csv"
)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>🏠 Luxury Housing Bangalore Dashboard | Data Analysis Platform</p>
    <p>Last Updated: 2025 | Data Records: {:,}</p>
</div>
""".format(len(df_filtered)), unsafe_allow_html=True)
