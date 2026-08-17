import pandas as pd
import matplotlib.pyplot as plt

# Load master dataset
df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

print("=" * 60)
print("NIGERIA ECONOMIC INTELLIGENCE DATASET")
print("=" * 60)

print("\nDataset shape:")
print(df.shape)

print("\nColumns:")
print(df.columns.tolist())

print("\nData types:")
print(df.dtypes)

print("\nMissing values:")
print(df.isna().sum())

print("\nSummary statistics:")
print(df.describe().round(2))

print("\nLatest available data:")
print(df.tail(5))

# Create reports folder if necessary
import os
os.makedirs("reports/figures", exist_ok=True)

# -----------------------------
# Inflation chart
# -----------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    df["year"],
    df["inflation_rate"]
)

plt.title("Nigeria Inflation Rate")
plt.xlabel("Year")
plt.ylabel("Inflation Rate (%)")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/inflation_history.png",
    dpi=300
)

plt.close()

# -----------------------------
# Exchange rate chart
# -----------------------------
plt.figure(figsize=(12, 6))

plt.plot(
    df["year"],
    df["exchange_rate"]
)

plt.title("Nigeria Official Exchange Rate")
plt.xlabel("Year")
plt.ylabel("Naira per US Dollar")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/exchange_rate_history.png",
    dpi=300
)

plt.close()

# -----------------------------
# GDP growth chart
# -----------------------------
plt.figure(figsize=(12, 6))

plt.axhline(
    y=0,
    linewidth=1
)

plt.plot(
    df["year"],
    df["gdp_growth"]
)

plt.title("Nigeria GDP Growth")
plt.xlabel("Year")
plt.ylabel("GDP Growth (%)")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/gdp_growth_history.png",
    dpi=300
)

plt.close()

print("\nEDA completed successfully!")
print("Charts saved in reports/figures/")
