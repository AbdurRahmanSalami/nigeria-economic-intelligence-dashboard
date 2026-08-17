import json
import pandas as pd

with open("data/raw/world_bank/exchange_rate.json", "r") as file:
    raw_data = json.load(file)

records = raw_data[1]

data = []

for record in records:
    if record["value"] is not None:
        data.append({
            "year": int(record["date"]),
            "exchange_rate": float(record["value"])
        })

df = pd.DataFrame(data)

df = df.sort_values("year")

df.to_csv(
    "data/processed/nigeria_exchange_rate.csv",
    index=False
)

print("Exchange-rate data cleaned successfully!")
print()
print(df.tail(10))
print()
print(f"Total observations: {len(df)}")
print(f"Years: {df['year'].min()} - {df['year'].max()}")
