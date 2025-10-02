# ESG Score Prediction & Sustainable Corporate Analysis
# Hackathon Ready Script - Upload to GitHub
# -----------------------------------------------------

# 1. Import Libraries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Settings
plt.rcParams['figure.figsize'] = (10, 6)
sns.set_style('whitegrid')

# 2. Load Data
data_path = "company_esg_financial_dataset.csv"  # make sure file is in the same folder
df = pd.read_csv(data_path)

print("Shape:", df.shape)
print("Columns:", df.columns.tolist())
print(df.head())

# 3. Data Cleaning
df = df.drop_duplicates()
df.columns = [c.strip().lower() for c in df.columns]

# Rename for easier use
df = df.rename(columns={
    "companyid": "company_id",
    "companyname": "company_name",
    "industry": "industry",
    "region": "region",
    "year": "year",
    "revenue": "revenue",
    "profitmargin": "profit_margin",
    "marketcap": "market_cap",
    "growthrate": "growth_rate",
    "esg_overall": "esg_score",
    "esg_environmental": "esg_environment",
    "esg_social": "esg_social",
    "esg_governance": "esg_governance",
    "carbonemissions": "carbon_emissions",
    "waterusage": "water_usage",
    "energyconsumption": "energy_consumption"
})

# Convert to numeric
num_cols = ["revenue","profit_margin","market_cap","growth_rate",
            "esg_score","esg_environment","esg_social","esg_governance",
            "carbon_emissions","water_usage","energy_consumption"]
for col in num_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 4. Exploratory Data Analysis (EDA)

# Q1: ESG vs Carbon Emissions
fig1 = px.scatter(df, x="carbon_emissions", y="esg_score", trendline="ols",
                  title="ESG Score vs Carbon Emissions")
fig1.show()

# Q2: ESG vs Revenue
fig2 = px.scatter(df, x="revenue", y="esg_score", trendline="ols",
                  title="ESG Score vs Revenue")
fig2.show()

# Q3: Average ESG by Industry
industry_avg = df.groupby("industry")["esg_score"].mean().reset_index()
fig3 = px.bar(industry_avg.sort_values("esg_score", ascending=False),
              x="industry", y="esg_score", title="Average ESG Score by Industry")
fig3.show()

# Q4: ESG by Region
region_avg = df.groupby("region")["esg_score"].mean().reset_index()
fig4 = px.bar(region_avg.sort_values("esg_score", ascending=False),
              x="region", y="esg_score", title="Average ESG Score by Region")
fig4.show()

# Q5: ESG Trend Over Time
year_avg = df.groupby("year")["esg_score"].mean().reset_index()
fig5 = px.line(year_avg, x="year", y="esg_score", title="ESG Score Trend Over Time")
fig5.show()

# Q6: Correlation Heatmap
corr = df[num_cols].corr()
plt.figure(figsize=(10,8))
sns.heatmap(corr, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Correlation Heatmap (ESG & Financials)")
plt.show()

# 5. Insights (example to print out)
print("\n--- Key Insights ---")
print("1. Negative correlation between carbon emissions and ESG score → reducing emissions improves ESG.")
print("2. Higher revenue companies tend to show higher ESG scores → bigger firms invest in sustainability.")
print("3. Industry differences exist (e.g., Retail vs Energy).")
print("4. ESG performance varies across regions.")
print("5. ESG scores show gradual improvement over years.")

# 6. Policy Recommendations
print("\n--- Policy Recommendations ---")
print("1. Set carbon reduction targets per industry.")
print("2. Incentivize water and energy efficiency.")
print("3. Link executive compensation to ESG KPIs.")
print("4. Encourage transparency in governance practices.")
print("5. Share regional best practices to raise ESG globally.")

# -----------------------------------------------------
# Next Step: Build a dashboard
# (Optional) Create a Streamlit app for interactive visuals
# Save this as streamlit_app.py and run: streamlit run streamlit_app.py
