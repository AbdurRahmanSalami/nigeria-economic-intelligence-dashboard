import pandas as pd

# Load all cleaned datasets
inflation = pd.read_csv("data/processed/nigeria_inflation.csv")
exchange = pd.read_csv("data/processed/nigeria_exchange_rate.csv")
gdp = pd.read_csv("data/processed/nigeria_gdp_growth.csv")
unemployment = pd.read_csv("data/processed/nigeria_unemployment.csv")
oil_rents = pd.read_csv("data/processed/nigeria_oil_rents.csv")
reserves = pd.read_csv("data/processed/nigeria_reserves.csv")
current_account = pd.read_csv(
    "data/processed/nigeria_current_account.csv"
)

# Merge all indicators
df = pd.merge(inflation, exchange, on="year", how="outer")
df = pd.merge(df, gdp, on="year", how="outer")
df = pd.merge(df, unemployment, on="year", how="outer")
df = pd.merge(df, oil_rents, on="year", how="outer")
df = pd.merge(df, reserves, on="year", how="outer")
df = pd.merge(df, current_account, on="year", how="outer")

# Sort chronologically
df = df.sort_values("year")

# Save final master dataset
df.to_csv(
    "data/processed/nigeria_economic_data.csv",
    index=False
)

print("Final master economic dataset created successfully!")
print()
print(df.tail(10))
print()
print("Columns:")
print(df.columns.tolist())
print()
print(f"Total rows: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
print()
print("Missing values:")
print(df.isna().sum())
