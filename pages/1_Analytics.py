import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Config
# -----------------------------------

st.set_page_config(
    page_title="Analytics",
    page_icon="📈",
    layout="wide"
)

st.title("📈 Advanced Analytics")

# -----------------------------------
# Load Data
# -----------------------------------

uploaded = st.sidebar.file_uploader(
    "Upload CSV",
    type=["csv"]
)

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("data/sales_data.csv")

df["Date"] = pd.to_datetime(df["Date"])

# -----------------------------------
# Sidebar Filters
# -----------------------------------

st.sidebar.header("Analytics Filters")

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

if region != "All":
    df = df[df["Region"] == region]

if category != "All":
    df = df[df["Category"] == category]

if df.empty:
    st.warning("No data available.")
    st.stop()

# -----------------------------------
# Revenue Heatmap
# -----------------------------------

st.subheader("🔥 Revenue Heatmap")

heat = pd.pivot_table(
    df,
    values="Sales",
    index="Region",
    columns="Category",
    aggfunc="sum",
    fill_value=0
)

st.dataframe(
    heat.style.background_gradient(cmap="Blues"),
    use_container_width=True
)

# -----------------------------------
# Monthly Revenue Trend
# -----------------------------------

st.subheader("📈 Monthly Revenue Trend")

monthly = (
    df.groupby(df["Date"].dt.to_period("M"))["Sales"]
    .sum()
    .reset_index()
)

monthly["Date"] = monthly["Date"].astype(str)

fig = px.line(
    monthly,
    x="Date",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend"
)

fig.update_layout(
    transition_duration=700
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Sales Distribution
# -----------------------------------

st.subheader("📊 Sales Distribution")

fig2 = px.histogram(
    df,
    x="Sales",
    nbins=30,
    title="Distribution of Sales"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Quantity Box Plot
# -----------------------------------

st.subheader("📦 Quantity Distribution")

fig3 = px.box(
    df,
    y="Quantity",
    title="Quantity Box Plot"
)

st.plotly_chart(
    fig3,
    use_container_width=True
)

# -----------------------------------
# Product Revenue
# -----------------------------------

st.subheader("🏆 Product Revenue")

product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .reset_index()
)

fig4 = px.bar(
    product_sales,
    x="Product",
    y="Sales",
    color="Product",
    title="Revenue by Product"
)

st.plotly_chart(
    fig4,
    use_container_width=True
)

# -----------------------------------
# Category Share
# -----------------------------------

st.subheader("🥧 Category Share")

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig5 = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    hole=0.45
)

st.plotly_chart(
    fig5,
    use_container_width=True
)

# -----------------------------------
# Correlation Matrix
# -----------------------------------

st.subheader("📉 Correlation Matrix")

corr = df[["Sales", "Quantity"]].corr()

st.dataframe(
    corr.style.background_gradient(cmap="Greens"),
    use_container_width=True
)

# -----------------------------------
# Optional Map
# -----------------------------------

if "Latitude" in df.columns and "Longitude" in df.columns:

    st.subheader("🗺️ Sales Map")

    map_df = df.rename(
        columns={
            "Latitude": "lat",
            "Longitude": "lon"
        }
    )

    st.map(map_df)

else:

    st.info(
        "Add Latitude and Longitude columns to your dataset to enable the interactive map."
    )

# -----------------------------------
# Summary Statistics
# -----------------------------------

st.subheader("📋 Dataset Summary")

st.dataframe(
    df.describe(),
    use_container_width=True
)

# -----------------------------------
# Download
# -----------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Analytics Data",
    csv,
    "analytics.csv",
    "text/csv"
)

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.caption(
    "Analytics Page | Streamlit Business Intelligence Dashboard"
)