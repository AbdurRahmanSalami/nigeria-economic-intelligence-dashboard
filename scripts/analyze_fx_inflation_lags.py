import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

# Calculate annual percentage change in exchange rate
# Positive values mean the naira weakened against the dollar.
df["fx_change_pct"] = (
    df["exchange_rate"].pct_change() * 100
)

# Focus on a common modern period
df = df[
    (df["year"] >= 1991) &
    (df["year"] <= 2025)
].copy()

results = []

for lag in range(4):

    # Previous FX movement aligned with current inflation
    df[f"fx_lag_{lag}"] = df["fx_change_pct"].shift(lag)

    temp = df[
        ["inflation_rate", f"fx_lag_{lag}"]
    ].dropna()

    correlation = temp["inflation_rate"].corr(
        temp[f"fx_lag_{lag}"]
    )

    results.append({
        "lag_years": lag,
        "correlation": correlation,
        "observations": len(temp)
    })

results_df = pd.DataFrame(results)

print("=" * 65)
print("FX DEPRECIATION VS INFLATION — LAG ANALYSIS")
print("=" * 65)
print()
print(results_df.round(3).to_string(index=False))

results_df.to_csv(
    "reports/fx_inflation_lag_analysis.csv",
    index=False
)

# Create chart
os.makedirs("reports/figures", exist_ok=True)

plt.figure(figsize=(9, 6))

plt.bar(
    results_df["lag_years"],
    results_df["correlation"]
)

plt.axhline(
    y=0,
    linewidth=1
)

plt.title("Exchange-Rate Change vs Inflation: Lag Analysis")
plt.xlabel("FX Change Lag (Years)")
plt.ylabel("Correlation with Inflation")
plt.xticks([0, 1, 2, 3])
plt.ylim(-1, 1)
plt.grid(axis="y", alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/fx_inflation_lag_analysis.png",
    dpi=300
)

plt.close()

best = results_df.loc[
    results_df["correlation"].abs().idxmax()
]

print()
print(
    f"Strongest relationship: lag {int(best['lag_years'])} "
    f"with correlation {best['correlation']:.3f}"
)

print()
print("FX-inflation lag analysis completed successfully!")
