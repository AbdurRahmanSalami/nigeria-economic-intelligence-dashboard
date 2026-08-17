import os
import warnings
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_absolute_error, mean_squared_error

warnings.filterwarnings("ignore")

# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

inflation = df[
    ["year", "inflation_rate"]
].dropna().copy()

inflation = inflation.sort_values("year")

# --------------------------------------------------
# Train/test split
#
# Train: everything before 2016
# Test: 2016-2025
#
# We do NOT randomly split time-series data.
# --------------------------------------------------

train = inflation[inflation["year"] < 2016].copy()
test = inflation[inflation["year"] >= 2016].copy()

print("=" * 70)
print("NIGERIA INFLATION FORECASTING")
print("=" * 70)

print()
print(f"Training period: {train['year'].min()} - {train['year'].max()}")
print(f"Testing period:  {test['year'].min()} - {test['year'].max()}")
print(f"Training observations: {len(train)}")
print(f"Testing observations:  {len(test)}")

# --------------------------------------------------
# Baseline model
#
# Predict every test year using the final training
# year's inflation rate.
# --------------------------------------------------

baseline_value = train["inflation_rate"].iloc[-1]

baseline_predictions = np.repeat(
    baseline_value,
    len(test)
)

baseline_mae = mean_absolute_error(
    test["inflation_rate"],
    baseline_predictions
)

baseline_rmse = np.sqrt(
    mean_squared_error(
        test["inflation_rate"],
        baseline_predictions
    )
)

# --------------------------------------------------
# ARIMA model
# --------------------------------------------------

model = ARIMA(
    train["inflation_rate"],
    order=(2, 1, 1)
)

model_fit = model.fit()

arima_predictions = model_fit.forecast(
    steps=len(test)
)

arima_mae = mean_absolute_error(
    test["inflation_rate"],
    arima_predictions
)

arima_rmse = np.sqrt(
    mean_squared_error(
        test["inflation_rate"],
        arima_predictions
    )
)

# --------------------------------------------------
# Display evaluation
# --------------------------------------------------

print()
print("MODEL PERFORMANCE")
print("-" * 70)

print(
    f"Baseline MAE:  {baseline_mae:.2f}"
)

print(
    f"Baseline RMSE: {baseline_rmse:.2f}"
)

print()

print(
    f"ARIMA MAE:     {arima_mae:.2f}"
)

print(
    f"ARIMA RMSE:    {arima_rmse:.2f}"
)

if arima_mae < baseline_mae:
    print()
    print("ARIMA outperformed the baseline on MAE.")
else:
    print()
    print("The baseline outperformed ARIMA on MAE.")

# --------------------------------------------------
# Save test predictions
# --------------------------------------------------

results = pd.DataFrame({
    "year": test["year"].values,
    "actual_inflation": test["inflation_rate"].values,
    "baseline_prediction": baseline_predictions,
    "arima_prediction": arima_predictions.values
})

os.makedirs("reports", exist_ok=True)

results.to_csv(
    "reports/inflation_backtest.csv",
    index=False
)

# --------------------------------------------------
# Plot backtest
# --------------------------------------------------

os.makedirs(
    "reports/figures",
    exist_ok=True
)

plt.figure(figsize=(12, 6))

plt.plot(
    inflation["year"],
    inflation["inflation_rate"],
    label="Actual"
)

plt.plot(
    test["year"],
    arima_predictions,
    marker="o",
    label="ARIMA forecast"
)

plt.axvline(
    x=2015,
    linestyle="--",
    linewidth=1
)

plt.title(
    "Nigeria Inflation Forecast Backtest"
)

plt.xlabel("Year")
plt.ylabel("Inflation Rate (%)")

plt.legend()
plt.grid(alpha=0.3)

plt.tight_layout()

plt.savefig(
    "reports/figures/inflation_backtest.png",
    dpi=300
)

plt.close()

print()
print("Backtest results saved successfully.")
