# streamlit_app.py
# -----------------------------------------------------
# Interactive Dashboard for ESG & Financial Analysis
# Hackathon-ready (upload along with ESG_EDA.py)
# -----------------------------------------------------

import streamlit as st
import pandas as pd
import plotly.express as px

# Load Data
@st.cache_data
def load_data():
    return pd.read_csv("company_esg_financial_dataset.csv")

df = load_data()

# Page Config
st.set_page_config(page_title="ESG Dashboard", layout="wide")
st.title("🌍 ESG & Financial Performance Dashboard")

# Sidebar Filters
st.sidebar.header("🔎 Filters")
industries = st.sidebar.multiselect("Select Industries", options=df["Industry"].unique(),
                                    default=df["Industry"].unique())
regions = st.sidebar.multiselect("Select Regions", options=df["Region"].unique(),
                                 default=df["Region"].unique())
years = st.sidebar.slider("Select Year Range",
                          int(df["Year"].min()), int(df["Year"].max()),
                          (int(df["Year"].min()), int(df["Year"].max())))

# Apply filters
df_filtered = df[
    (df["Industry"].isin(industries)) &
    (df["Region"].isin(regions)) &
    (df["Year"].between(years[0], years[1]))
]

# Tabs for analysis
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Overview", "ESG vs Carbon", "Industry & Region", "Trends", "Correlation"
])

# Tab 1: Overview
with tab1:
    st.subheader("Dataset Overview")
    st.write(df_filtered.describe())

    st.metric("Average ESG Score", round(df_filtered["ESG_Overall"].mean(),2))
    st.metric("Average Revenue", round(df_filtered["Revenue"].mean(),2))
    st.metric("Average Carbon Emissions", round(df_filtered["CarbonEmissions"].mean(),2))

# Tab 2: ESG vs Carbon
with tab2:
    st.subheader("ESG Score vs Carbon Emissions")
    fig = px.scatter(df_filtered, x="CarbonEmissions", y="ESG_Overall",
                     color="Industry", trendline="ols",
                     title="Carbon Emissions vs ESG Score")
    st.plotly_chart(fig, use_container_width=True)

# Tab 3: Industry & Region
with tab3:
    st.subheader("Average ESG by Industry")
    ind_avg = df_filtered.groupby("Industry")["ESG_Overall"].mean().reset_index()
    fig1 = px.bar(ind_avg.sort_values("ESG_Overall", ascending=False),
                  x="Industry", y="ESG_Overall", title="Industry-wise ESG Score")
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("Average ESG by Region")
    reg_avg = df_filtered.groupby("Region")["ESG_Overall"].mean().reset_index()
    fig2 = px.bar(reg_avg.sort_values("ESG_Overall", ascending=False),
                  x="Region", y="ESG_Overall", title="Region-wise ESG Score")
    st.plotly_chart(fig2, use_container_width=True)

# Tab 4: Trends
with tab4:
    st.subheader("ESG Score Over Time")
    year_avg = df_filtered.groupby("Year")["ESG_Overall"].mean().reset_index()
    fig3 = px.line(year_avg, x="Year", y="ESG_Overall", title="Trend of ESG Score Over Years")
    st.plotly_chart(fig3, use_container_width=True)

    st.subheader("Revenue vs ESG Over Time")
    fig4 = px.scatter(df_filtered, x="Revenue", y="ESG_Overall",
                      color="Year", trendline="ols")
    st.plotly_chart(fig4, use_container_width=True)

# Tab 5: Correlation Heatmap
with tab5:
    st.subheader("Correlation Matrix")
    corr = df_filtered[["Revenue","ProfitMargin","MarketCap","GrowthRate",
                        "ESG_Overall","ESG_Environmental","ESG_Social",
                        "ESG_Governance","CarbonEmissions","WaterUsage","EnergyConsumption"]].corr()
    fig5 = px.imshow(corr, text_auto=True, aspect="auto", title="Correlation Heatmap")
    st.plotly_chart(fig5, use_container_width=True)

# -----------------------------------------------------
# Run this app: 
#    streamlit run streamlit_app.py
# -----------------------------------------------------
