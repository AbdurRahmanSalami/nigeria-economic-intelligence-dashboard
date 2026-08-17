import os
import warnings
import pandas as pd
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA

warnings.filterwarnings("ignore")

# --------------------------------------------------
# Load inflation data
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

inflation = (
    df[["year", "inflation_rate"]]
    .dropna()
    .sort_values("year")
)

print("=" * 70)
print("NIGERIA INFLATION FORECAST: 2026-2030")
print("=" * 70)

print()
print(
    f"Historical data: "
    f"{inflation['year'].min()} - {inflation['year'].max()}"
)

print(
    f"Observations: {len(inflation)}"
)

# --------------------------------------------------
# Train winning model on full dataset
# --------------------------------------------------

model = ARIMA(
    inflation["inflation_rate"],
    order=(1, 1, 1)
)

model_fit = model.fit()

# --------------------------------------------------
# Forecast next 5 years
# --------------------------------------------------

forecast_result = model_fit.get_forecast(
    steps=5
)

forecast_mean = forecast_result.predicted_mean

confidence = forecast_result.conf_int(
    alpha=0.05
)

future_years = [
    2026,
    2027,
    2028,
    2029,
    2030
]

forecast_df = pd.DataFrame({
    "year": future_years,
    "forecast_inflation": forecast_mean.values,
    "lower_95": confidence.iloc[:, 0].values,
    "upper_95": confidence.iloc[:, 1].values
})

forecast_df[
    [
        "forecast_inflation",
        "lower_95",
        "upper_95"
    ]
] = forecast_df[
    [
        "forecast_inflation",
        "lower_95",
        "upper_95"
    ]
].round(2)

# --------------------------------------------------
# Display forecast
# --------------------------------------------------

print()
print("FORECAST")
print("-" * 70)
print()
print(
    forecast_df.to_string(
        index=False
    )
)

# --------------------------------------------------
# Save forecast
# --------------------------------------------------

os.makedirs("reports", exist_ok=True)

forecast_df.to_csv(
    "reports/inflation_forecast_2026_2030.csv",
    index=False
)

# --------------------------------------------------
# Create forecast chart
# --------------------------------------------------

os.makedirs(
    "reports/figures",
    exist_ok=True
)

# Show recent history rather than all 66 years
history = inflation[
    inflation["year"] >= 1990
]

plt.figure(figsize=(12, 6))

plt.plot(
    history["year"],
    history["inflation_rate"],
    marker="o",
    label="Historical inflation"
)

plt.plot(
    forecast_df["year"],
    forecast_df["forecast_inflation"],
    marker="o",
    linestyle="--",
    label="ARIMA forecast"
)

plt.fill_between(
    forecast_df["year"],
    forecast_df["lower_95"],
    forecast_df["upper_95"],
    alpha=0.2,
    label="95% confidence interval"
)

plt.axvline(
    x=2025,
    linestyle="--",
    linewidth=1
)

plt.title(
    "Nigeria Inflation: Historical Data and ARIMA Forecast"
)

plt.xlabel("Year")
plt.ylabel("Inflation Rate (%)")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/inflation_forecast_2026_2030.png",
    dpi=300
)

plt.close()

print()
print(
    "Forecast saved to "
    "reports/inflation_forecast_2026_2030.csv"
)

print(
    "Chart saved to "
    "reports/figures/inflation_forecast_2026_2030.png"
)
