import json
import pandas as pd

# Load raw World Bank current-account data
with open("data/raw/world_bank/current_account.json", "r") as file:
    raw_data = json.load(file)

records = raw_data[1]

data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "current_account_pct_gdp": float(record["value"])
        })

df = pd.DataFrame(data)

# Sort oldest to newest
df = df.sort_values("year")

# Round for readability
df["current_account_pct_gdp"] = df["current_account_pct_gdp"].round(2)

# Save cleaned dataset
df.to_csv(
    "data/processed/nigeria_current_account.csv",
    index=False
)

print("Current-account data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
