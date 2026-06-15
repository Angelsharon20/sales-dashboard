import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="Reports",
    page_icon="📑",
    layout="wide"
)

st.title("📑 Reports & Data Export")

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
# Date Filter
# -----------------------------------

st.sidebar.header("Date Filter")

start = st.sidebar.date_input(
    "Start Date",
    df["Date"].min()
)

end = st.sidebar.date_input(
    "End Date",
    df["Date"].max()
)

df = df[
    (df["Date"] >= pd.to_datetime(start)) &
    (df["Date"] <= pd.to_datetime(end))
]

if df.empty:
    st.warning("No records available.")
    st.stop()

# -----------------------------------
# Report Summary
# -----------------------------------

st.subheader("📊 Report Summary")

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
c2.metric("Orders", df["OrderID"].nunique())
c3.metric("Products", df["Product"].nunique())
c4.metric("Regions", df["Region"].nunique())

# -----------------------------------
# Sales by Region
# -----------------------------------

st.subheader("🌍 Sales by Region")

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .reset_index()
)

fig = px.bar(
    region_sales,
    x="Region",
    y="Sales",
    color="Region",
    text="Sales"
)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------------
# Sales by Category
# -----------------------------------

st.subheader("📦 Sales by Category")

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
    .reset_index()
)

fig2 = px.pie(
    category_sales,
    names="Category",
    values="Sales",
    hole=0.4
)

st.plotly_chart(fig2, use_container_width=True)

# -----------------------------------
# Pivot Table
# -----------------------------------

st.subheader("📋 Pivot Report")

pivot = pd.pivot_table(
    df,
    values="Sales",
    index="Region",
    columns="Category",
    aggfunc="sum",
    fill_value=0
)

st.dataframe(
    pivot,
    use_container_width=True
)

# -----------------------------------
# Summary Statistics
# -----------------------------------

st.subheader("📈 Statistical Summary")

st.dataframe(
    df.describe(),
    use_container_width=True
)

# -----------------------------------
# Complete Dataset
# -----------------------------------

st.subheader("🗂 Complete Dataset")

st.dataframe(
    df,
    use_container_width=True
)

# -----------------------------------
# Export CSV
# -----------------------------------

csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download CSV Report",
    csv,
    "sales_report.csv",
    "text/csv"
)

# -----------------------------------
# Export Excel
# -----------------------------------

from io import BytesIO

buffer = BytesIO()

with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
    df.to_excel(writer, index=False)

st.download_button(
    "📥 Download Excel Report",
    buffer.getvalue(),
    "sales_report.xlsx",
    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
)

# -----------------------------------
# Top Products
# -----------------------------------

st.subheader("🏆 Top Products")

top = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.bar_chart(top)

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.caption(
    "Reports Module | Sales Dashboard"
)