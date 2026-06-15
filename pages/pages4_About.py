import streamlit as st

# -----------------------------------
# Page Configuration
# -----------------------------------

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

# -----------------------------------
# Title
# -----------------------------------

st.title("ℹ️ About This Project")

st.markdown("---")

# -----------------------------------
# Project Overview
# -----------------------------------

st.header("📊 Sales & Revenue Analysis Dashboard")

st.write("""
The **Sales & Revenue Analysis Dashboard** is an interactive Business Intelligence
application built using **Streamlit, Pandas, and Plotly**.

It helps users analyze sales performance through KPIs, charts, filters,
AI-generated insights, downloadable reports, and interactive visualizations.
""")

# -----------------------------------
# Technologies Used
# -----------------------------------

st.header("💻 Technologies Used")

tech1, tech2, tech3 = st.columns(3)

with tech1:
    st.success("""
    - Python
    - Pandas
    - NumPy
    """)

with tech2:
    st.success("""
    - Streamlit
    - Plotly
    - OpenPyXL
    """)

with tech3:
    st.success("""
    - CSV Processing
    - Data Visualization
    - Business Analytics
    """)

# -----------------------------------
# Features
# -----------------------------------

st.header("✨ Key Features")

features = [
    "📁 CSV Upload",
    "📅 Year / Quarter / Month Filters",
    "🌍 Region Filters",
    "📦 Product & Category Filters",
    "💰 KPI Cards",
    "📈 Monthly Revenue Trends",
    "🎯 Sales Target Gauge",
    "📊 Interactive Charts",
    "🤖 AI Business Insights",
    "📋 Reports & Analytics",
    "📥 CSV / Excel Export",
    "🏆 Top Products Analysis",
    "📉 Growth Analysis",
    "🔥 Revenue Heatmaps",
]

for feature in features:
    st.write(feature)

# -----------------------------------
# Skills Demonstrated
# -----------------------------------

st.header("🚀 Skills Demonstrated")

skills = [
    "Data Analysis",
    "Business Intelligence",
    "Dashboard Development",
    "Data Visualization",
    "Python Programming",
    "Pandas Data Processing",
    "Plotly Charts",
    "Streamlit Web Apps",
    "KPI Reporting",
    "Interactive Filtering",
]

st.write(", ".join(skills))

# -----------------------------------
# Resume Description
# -----------------------------------

st.header("📝 Resume Project Description")

resume_text = """
Developed a Sales & Revenue Analysis Dashboard using Streamlit, Pandas,
and Plotly to analyze business performance through KPI metrics,
interactive charts, AI-powered insights, filtering capabilities,
and downloadable reports.

Implemented dynamic dashboards with CSV upload support,
advanced analytics, sales forecasting, and executive reporting
to improve business decision-making.
"""

st.info(resume_text)

# -----------------------------------
# Project Statistics
# -----------------------------------

st.header("📊 Project Statistics")

c1, c2, c3 = st.columns(3)

c1.metric("Pages", "4")
c2.metric("Technologies", "5+")
c3.metric("Visualizations", "10+")

# -----------------------------------
# Future Improvements
# -----------------------------------

st.header("🔮 Future Enhancements")

future = [
    "Machine Learning Forecasting",
    "Database Integration (MySQL/PostgreSQL)",
    "User Authentication",
    "Real-time Data Streaming",
    "Power BI Style Themes",
    "Interactive Maps",
    "Automated Email Reports",
    "Cloud Deployment",
    "REST API Integration",
    "Predictive Analytics",
]

for item in future:
    st.write("✅", item)

# -----------------------------------
# Contact Section
# -----------------------------------

st.header("👤 Developer")

st.write("**Name:** Angel Sharon")

st.write("**Role:** AI & Data Science Student")

st.write("**Project:** Sales & Revenue Analysis Dashboard")

st.write("**Built With:** ❤️ Python + Streamlit")

# -----------------------------------
# GitHub / LinkedIn
# -----------------------------------

st.header("🔗 Portfolio Links")

st.write("GitHub: https://github.com/angelsharon20")

st.write("LinkedIn: https://linkedin.com/in/angelsharon20")

st.caption("Replace the above links with your actual GitHub and LinkedIn profiles.")

# -----------------------------------
# Footer
# -----------------------------------

st.markdown("---")

st.success("Thank you for exploring the Sales & Revenue Analysis Dashboard!")

st.caption("© 2026 Angel Sharon | Business Intelligence Dashboard")