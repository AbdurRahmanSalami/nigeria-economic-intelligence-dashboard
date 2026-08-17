import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

os.makedirs("reports/figures", exist_ok=True)

# --------------------------------------------------
# Correlation matrix
# --------------------------------------------------

numeric_columns = [
    "inflation_rate",
    "exchange_rate",
    "gdp_growth",
    "unemployment_rate",
    "oil_rents_pct_gdp",
    "reserves_usd_billion",
    "current_account_pct_gdp"
]

correlation = df[numeric_columns].corr()

print("=" * 60)
print("CORRELATION MATRIX")
print("=" * 60)
print()
print(correlation.round(2))

correlation.to_csv(
    "reports/correlation_matrix.csv"
)

# --------------------------------------------------
# Inflation vs exchange rate
# Use percentage change in exchange rate because
# raw exchange-rate levels trend strongly over time.
# --------------------------------------------------

df["exchange_rate_change_pct"] = (
    df["exchange_rate"].pct_change() * 100
)

analysis_df = df.dropna(
    subset=["inflation_rate", "exchange_rate_change_pct"]
)

plt.figure(figsize=(10, 6))

plt.scatter(
    analysis_df["exchange_rate_change_pct"],
    analysis_df["inflation_rate"]
)

plt.title("Inflation vs Annual Exchange-Rate Change")
plt.xlabel("Exchange Rate Change (%)")
plt.ylabel("Inflation Rate (%)")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/inflation_vs_exchange_change.png",
    dpi=300
)

plt.close()

# --------------------------------------------------
# Inflation vs GDP growth
# --------------------------------------------------

analysis_df = df.dropna(
    subset=["inflation_rate", "gdp_growth"]
)

plt.figure(figsize=(10, 6))

plt.scatter(
    analysis_df["inflation_rate"],
    analysis_df["gdp_growth"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title("Inflation vs GDP Growth")
plt.xlabel("Inflation Rate (%)")
plt.ylabel("GDP Growth (%)")
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/inflation_vs_gdp_growth.png",
    dpi=300
)

plt.close()

print()
print("Relationship analysis completed successfully!")
print("Correlation matrix saved to reports/correlation_matrix.csv")
print("Charts saved to reports/figures/")
