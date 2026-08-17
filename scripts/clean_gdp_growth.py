import json
import pandas as pd

# Load raw World Bank GDP data
with open("data/raw/world_bank/gdp_growth.json", "r") as file:
    raw_data = json.load(file)

records = raw_data[1]

data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "gdp_growth": float(record["value"])
        })

df = pd.DataFrame(data)

# Sort from oldest to newest
df = df.sort_values("year")

# Save cleaned GDP dataset
df.to_csv(
    "data/processed/nigeria_gdp_growth.csv",
    index=False
)

print("GDP growth data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
