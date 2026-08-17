import json
import pandas as pd

# Load raw World Bank oil-rents data
with open("data/raw/world_bank/oil_rents.json", "r") as file:
    raw_data = json.load(file)

records = raw_data[1]

data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "oil_rents_pct_gdp": float(record["value"])
        })

df = pd.DataFrame(data)

# Sort oldest to newest
df = df.sort_values("year")

# Save cleaned dataset
df.to_csv(
    "data/processed/nigeria_oil_rents.csv",
    index=False
)

print("Oil-rents data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
