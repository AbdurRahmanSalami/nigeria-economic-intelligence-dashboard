import json
import pandas as pd

# Load raw World Bank JSON
with open("data/raw/world_bank/inflation.json", "r") as file:
    raw_data = json.load(file)

# World Bank response:
# raw_data[0] = metadata
# raw_data[1] = actual observations
records = raw_data[1]

# Extract the fields we need
data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "inflation_rate": float(record["value"])
        })

# Create dataframe
df = pd.DataFrame(data)

# Sort oldest to newest
df = df.sort_values("year")

# Save clean dataset
df.to_csv(
    "data/processed/nigeria_inflation.csv",
    index=False
)

print("Inflation data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
