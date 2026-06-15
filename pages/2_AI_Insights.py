import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="AI Insights",
    page_icon="🤖",
    layout="wide"
)

st.title("🤖 AI Business Insights Dashboard")

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
# Basic KPIs
# -----------------------------------

total_sales = df["Sales"].sum()
total_quantity = df["Quantity"].sum()
total_orders = df["OrderID"].nunique()

st.subheader("📊 Overall Performance")

c1, c2, c3 = st.columns(3)

c1.metric("💰 Total Sales", f"₹{total_sales:,.0f}")
c2.metric("📦 Quantity Sold", total_quantity)
c3.metric("🛒 Orders", total_orders)

# -----------------------------------
# Best Product
# -----------------------------------

product_sales = (
    df.groupby("Product")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

best_product = product_sales.idxmax()
best_product_sales = product_sales.max()

st.success(
    f"🏆 Best Selling Product: **{best_product}** "
    f"(₹{best_product_sales:,.0f})"
)

# -----------------------------------
# Worst Product
# -----------------------------------

worst_product = product_sales.idxmin()
worst_product_sales = product_sales.min()

st.warning(
    f"📉 Lowest Selling Product: **{worst_product}** "
    f"(₹{worst_product_sales:,.0f})"
)

# -----------------------------------
# Best Region
# -----------------------------------

region_sales = (
    df.groupby("Region")["Sales"]
    .sum()
    .sort_values(ascending=False)
)

best_region = region_sales.idxmax()

st.info(
    f"🌍 Highest Revenue Region: **{best_region}**"
)

# -----------------------------------
# Best Category
# -----------------------------------

category_sales = (
    df.groupby("Category")["Sales"]
    .sum()
)

best_category = category_sales.idxmax()
worst_category = category_sales.idxmin()

st.success(
    f"📈 Best Category: **{best_category}**"
)

st.error(
    f"📉 Weakest Category: **{worst_category}**"
)

# -----------------------------------
# Month-over-Month Growth
# -----------------------------------

monthly = (
    df.groupby(df["Date"].dt.to_period("M"))["Sales"]
    .sum()
)

if len(monthly) >= 2:

    current = monthly.iloc[-1]
    previous = monthly.iloc[-2]

    if previous != 0:

        growth = ((current - previous) / previous) * 100

        if growth > 0:

            st.success(
                f"📈 Growth increased by {growth:.2f}% compared to previous month."
            )

        else:

            st.error(
                f"📉 Growth decreased by {abs(growth):.2f}% compared to previous month."
            )

# -----------------------------------
# Product Contribution
# -----------------------------------

st.subheader("🏆 Product Contribution")

fig = px.pie(
    df,
    names="Product",
    values="Sales",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------------
# Region Comparison
# -----------------------------------

st.subheader("🌍 Region Comparison")

fig2 = px.bar(
    region_sales.reset_index(),
    x="Region",
    y="Sales",
    color="Region",
    title="Sales by Region"
)

st.plotly_chart(
    fig2,
    use_container_width=True
)

# -----------------------------------
# Smart Recommendations
# -----------------------------------

st.subheader("💡 AI Recommendations")

recommendations = []

recommendations.append(
    f"Increase marketing efforts for **{worst_category}**."
)

recommendations.append(
    f"Maintain inventory levels for **{best_product}**."
)

recommendations.append(
    f"Expand operations in **{best_region}** due to high demand."
)

recommendations.append(
    f"Bundle **{worst_product}** with popular products to improve sales."
)

recommendations.append(
    "Offer seasonal discounts during low-performing months."
)

for rec in recommendations:
    st.write("✅", rec)

# -----------------------------------
# Risk Alerts
# -----------------------------------

st.subheader("🚨 Business Alerts")

avg_sales = df["Sales"].mean()

low_sales_products = product_sales[
    product_sales < avg_sales
]

if len(low_sales_products) > 0:

    st.warning(
        "The following products are performing below average:"
    )

    st.dataframe(low_sales_products)

else:

    st.success("No low-performing products detected.")

# -----------------------------------
# Forecast Hint
# -----------------------------------

st.subheader("🔮 Forecast")

forecast = total_sales * 1.10

st.info(
    f"If current trends continue, estimated future sales could reach "
    f"₹{forecast:,.0f}."
)

# -----------------------------------
# Executive Summary
# -----------------------------------

st.subheader("📝 Executive Summary")

summary = f"""

Total Sales: ₹{total_sales:,.0f}

Best Product: {best_product}

Best Region: {best_region}

Weakest Category: {worst_category}

Recommendation:

• Focus on improving {worst_category}

• Continue investing in {best_product}

• Expand in {best_region}

"""

st.text(summary)

# -----------------------------------
# Download Summary
# -----------------------------------

st.download_button(
    "📥 Download Executive Summary",
    summary,
    file_name="executive_summary.txt"
)

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.caption(
    "AI Insights | Sales & Revenue Dashboard"
)