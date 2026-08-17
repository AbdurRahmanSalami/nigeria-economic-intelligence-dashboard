import json
import pandas as pd

# Load raw World Bank reserves data
with open("data/raw/world_bank/reserves.json", "r") as file:
    raw_data = json.load(file)

records = raw_data[1]

data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "reserves_usd_billion": float(record["value"]) / 1_000_000_000
        })

df = pd.DataFrame(data)

# Sort oldest to newest
df = df.sort_values("year")

# Round for readability
df["reserves_usd_billion"] = df["reserves_usd_billion"].round(2)

# Save cleaned dataset
df.to_csv(
    "data/processed/nigeria_reserves.csv",
    index=False
)

print("Foreign-reserves data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
