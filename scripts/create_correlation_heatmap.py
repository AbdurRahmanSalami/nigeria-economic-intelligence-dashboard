import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

columns = [
    "inflation_rate",
    "exchange_rate",
    "gdp_growth",
    "unemployment_rate",
    "oil_rents_pct_gdp",
    "reserves_usd_billion",
    "current_account_pct_gdp"
]

labels = [
    "Inflation",
    "Exchange Rate",
    "GDP Growth",
    "Unemployment",
    "Oil Rents",
    "Reserves",
    "Current Account"
]

correlation = df[columns].corr()

# Print the complete matrix without truncation
print("=" * 90)
print("FULL CORRELATION MATRIX")
print("=" * 90)
print()
print(correlation.round(2).to_string())

os.makedirs("reports/figures", exist_ok=True)

# Create heatmap
fig, ax = plt.subplots(figsize=(11, 8))

image = ax.imshow(
    correlation,
    vmin=-1,
    vmax=1
)

ax.set_xticks(range(len(labels)))
ax.set_yticks(range(len(labels)))

ax.set_xticklabels(labels, rotation=45, ha="right")
ax.set_yticklabels(labels)

# Add values inside cells
for i in range(len(labels)):
    for j in range(len(labels)):
        ax.text(
            j,
            i,
            f"{correlation.iloc[i, j]:.2f}",
            ha="center",
            va="center"
        )

ax.set_title("Nigeria Economic Indicator Correlations")

fig.colorbar(
    image,
    ax=ax,
    label="Correlation"
)

plt.tight_layout()

plt.savefig(
    "reports/figures/correlation_heatmap.png",
    dpi=300
)

plt.close()

print()
print("Correlation heatmap created successfully!")
