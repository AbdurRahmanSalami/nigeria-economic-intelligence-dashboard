import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

# --------------------------------------------------
# Create change-based variables
# --------------------------------------------------

# Positive exchange-rate change = naira depreciation
df["exchange_rate_change_pct"] = (
    df["exchange_rate"].pct_change() * 100
)

df["reserves_change_pct"] = (
    df["reserves_usd_billion"].pct_change() * 100
)

# --------------------------------------------------
# Restrict analysis to period where all indicators
# overlap
# --------------------------------------------------

analysis = df[
    (df["year"] >= 1991) &
    (df["year"] <= 2021)
].copy()

columns = [
    "inflation_rate",
    "exchange_rate_change_pct",
    "gdp_growth",
    "unemployment_rate",
    "oil_rents_pct_gdp",
    "reserves_change_pct",
    "current_account_pct_gdp"
]

analysis = analysis[
    ["year"] + columns
].dropna()

print("=" * 90)
print("COMMON-PERIOD ECONOMIC ANALYSIS")
print("=" * 90)

print()
print(f"Years: {analysis['year'].min()} - {analysis['year'].max()}")
print(f"Complete observations: {len(analysis)}")

correlation = analysis[columns].corr()

print()
print("CORRELATION MATRIX")
print()
print(correlation.round(2).to_string())

correlation.to_csv(
    "reports/robust_correlation_matrix.csv"
)

# --------------------------------------------------
# Heatmap
# --------------------------------------------------

labels = [
    "Inflation",
    "FX Change",
    "GDP Growth",
    "Unemployment",
    "Oil Rents",
    "Reserves Change",
    "Current Account"
]

os.makedirs("reports/figures", exist_ok=True)

fig, ax = plt.subplots(figsize=(11, 8))

image = ax.imshow(
    correlation,
    vmin=-1,
    vmax=1
)

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))

ax.set_xticklabels(
    labels,
    rotation=45,
    ha="right"
)

ax.set_yticklabels(labels)

for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

ax.set_title(
    "Nigeria Economic Correlations, 1991–2021"
)

fig.colorbar(
    image,
    ax=ax,
    label="Correlation"
)

plt.tight_layout()

plt.savefig(
    "reports/figures/robust_correlation_heatmap.png",
    dpi=300
)

plt.close()

print()
print("Robust relationship analysis completed successfully!")
