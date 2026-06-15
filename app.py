import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Sales & Revenue Dashboard",
    page_icon="📊",
    layout="wide"
)

# -----------------------------
# Custom CSS
# -----------------------------
st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

div[data-testid="metric-container"] {
    background: rgba(255,255,255,0.08);
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 15px;
    padding: 18px;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.3);
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
# Title
# -----------------------------
st.title("📊 Sales & Revenue Analysis Dashboard")
st.caption(f"Last Updated: {datetime.now().strftime('%d %B %Y %H:%M')}")

# -----------------------------
# Sidebar Upload
# -----------------------------
uploaded_file = st.sidebar.file_uploader(
    "📁 Upload CSV",
    type=["csv"]
)

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
else:
    df = pd.read_csv("data/sales_data.csv")

# -----------------------------
# Date Processing
# -----------------------------
df["Date"] = pd.to_datetime(df["Date"])

df["Year"] = df["Date"].dt.year
df["Quarter"] = df["Date"].dt.quarter
df["Month"] = df["Date"].dt.strftime("%B")

# -----------------------------
# Sidebar Filters
# -----------------------------
st.sidebar.header("🔍 Filters")

year = st.sidebar.selectbox(
    "Year",
    ["All"] + sorted(df["Year"].unique().tolist())
)

quarter = st.sidebar.selectbox(
    "Quarter",
    ["All", 1, 2, 3, 4]
)

month = st.sidebar.selectbox(
    "Month",
    ["All"] + sorted(df["Month"].unique().tolist())
)

region = st.sidebar.selectbox(
    "Region",
    ["All"] + sorted(df["Region"].unique().tolist())
)

category = st.sidebar.selectbox(
    "Category",
    ["All"] + sorted(df["Category"].unique().tolist())
)

product = st.sidebar.selectbox(
    "Product",
    ["All"] + sorted(df["Product"].unique().tolist())
)

search = st.sidebar.text_input("🔎 Search Product")

# -----------------------------
# Apply Filters
# -----------------------------
if year != "All":
    df = df[df["Year"] == year]

if quarter != "All":
    df = df[df["Quarter"] == quarter]

if month != "All":
    df = df[df["Month"] == month]

if region != "All":
    df = df[df["Region"] == region]

if category != "All":
    df = df[df["Category"] == category]

if product != "All":
    df = df[df["Product"] == product]

if search:
    df = df[df["Product"].str.contains(search, case=False, na=False)]

if df.empty:
    st.warning("No records found for the selected filters.")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------
total_sales = df["Sales"].sum()
total_orders = df["OrderID"].nunique()
total_quantity = df["Quantity"].sum()
average_sale = df["Sales"].mean()
average_quantity = df["Quantity"].mean()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
c2.metric("🛒 Orders", total_orders)
c3.metric("📦 Quantity", total_quantity)
c4.metric("📈 Avg Sale", f"₹{average_sale:,.0f}")
c5.metric("📊 Avg Qty", f"{average_quantity:.2f}")

# -----------------------------
# Sales Target Gauge
# -----------------------------
sales_target = 10000000

gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=total_sales,
        number={"prefix": "₹"},
        title={"text": "Sales Target"},
        gauge={
            "axis": {"range": [0, sales_target]},
            "bar": {"color": "green"}
        }
    )
)

st.plotly_chart(gauge, use_container_width=True)

# -----------------------------
# Monthly Revenue
# -----------------------------
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
    title="📈 Monthly Revenue Trend"
)

fig.update_layout(transition_duration=600)

st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# Revenue by Category & Region
# -----------------------------
left, right = st.columns(2)

with left:

    category_sales = (
        df.groupby("Category")["Sales"]
        .sum()
        .reset_index()
    )

    fig2 = px.bar(
        category_sales,
        x="Category",
        y="Sales",
        color="Category",
        title="📊 Revenue by Category"
    )

    st.plotly_chart(fig2, use_container_width=True)

with right:

    region_sales = (
        df.groupby("Region")["Sales"]
        .sum()
        .reset_index()
    )

    fig3 = px.pie(
        region_sales,
        names="Region",
        values="Sales",
        hole=0.45,
        title="🌍 Region-wise Revenue"
    )

    st.plotly_chart(fig3, use_container_width=True)

# -----------------------------
# Top Products
# -----------------------------
st.subheader("🏆 Top 5 Products")

top_products = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(5)
)

st.bar_chart(top_products)

# -----------------------------
# Best Product / Region
# -----------------------------
best_product = (
    df.groupby("Product")["Sales"]
    .sum()
    .idxmax()
)

best_region = (
    df.groupby("Region")["Sales"]
    .sum()
    .idxmax()
)

col1, col2 = st.columns(2)

col1.success(f"🏅 Best Product: {best_product}")
col2.info(f"🌍 Best Region: {best_region}")

# -----------------------------
# Month-over-Month Growth
# -----------------------------
monthly_growth = (
    df.groupby(df["Date"].dt.to_period("M"))["Sales"]
    .sum()
)

if len(monthly_growth) >= 2:

    current = monthly_growth.iloc[-1]
    previous = monthly_growth.iloc[-2]

    if previous != 0:

        growth = ((current - previous) / previous) * 100

        st.metric(
            "📈 Growth",
            f"{growth:.2f}%"
        )

# -----------------------------
# AI Business Summary
# -----------------------------
worst_category = (
    df.groupby("Category")["Sales"]
    .sum()
    .idxmin()
)

st.subheader("🤖 AI Business Summary")

st.info(f"""
🏆 Highest Selling Product: **{best_product}**

🌍 Highest Revenue Region: **{best_region}**

📉 Lowest Performing Category: **{worst_category}**

💡 Recommendation:

Increase marketing for **{worst_category}**
while maintaining inventory for
**{best_product}**.
""")

# -----------------------------
# Sales Table
# -----------------------------
with st.expander("📋 View Sales Data"):

    st.dataframe(
        df,
        use_container_width=True
    )

# -----------------------------
# Download CSV
# -----------------------------
csv = df.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered CSV",
    csv,
    "filtered_sales.csv",
    "text/csv"
)

# -----------------------------
# Footer
# -----------------------------
st.markdown("---")

st.caption(
    "Developed by Angel Sharon | Streamlit Business Intelligence Dashboard"
)