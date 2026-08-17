import warnings
import pandas as pd
import numpy as np

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing,
    Holt
)

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

warnings.filterwarnings("ignore")

# --------------------------------------------------
# Load data
# --------------------------------------------------

df = pd.read_csv(
    "data/processed/nigeria_economic_data.csv"
)

inflation = df[
    ["year", "inflation_rate"]
].dropna().sort_values("year")

train = inflation[
    inflation["year"] < 2016
].copy()

test = inflation[
    inflation["year"] >= 2016
].copy()

actual = test["inflation_rate"].values

results = []

# --------------------------------------------------
# Helper function
# --------------------------------------------------

def evaluate(name, predictions):

    predictions = np.array(predictions)

    mae = mean_absolute_error(
        actual,
        predictions
    )

    rmse = np.sqrt(
        mean_squared_error(
            actual,
            predictions
        )
    )

    results.append({
        "model": name,
        "mae": mae,
        "rmse": rmse
    })


# --------------------------------------------------
# 1. Naive baseline
# --------------------------------------------------

naive_predictions = np.repeat(
    train["inflation_rate"].iloc[-1],
    len(test)
)

evaluate(
    "Naive Baseline",
    naive_predictions
)


# --------------------------------------------------
# 2. Simple Exponential Smoothing
# --------------------------------------------------

ses_model = SimpleExpSmoothing(
    train["inflation_rate"]
).fit(
    optimized=True
)

ses_predictions = ses_model.forecast(
    len(test)
)

evaluate(
    "Simple Exponential Smoothing",
    ses_predictions
)


# --------------------------------------------------
# 3. Holt trend model
# --------------------------------------------------

holt_model = Holt(
    train["inflation_rate"],
    damped_trend=True
).fit(
    optimized=True
)

holt_predictions = holt_model.forecast(
    len(test)
)

evaluate(
    "Holt Damped Trend",
    holt_predictions
)


# --------------------------------------------------
# 4. ARIMA (1,1,1)
# --------------------------------------------------

arima_111 = ARIMA(
    train["inflation_rate"],
    order=(1, 1, 1)
).fit()

pred_111 = arima_111.forecast(
    len(test)
)

evaluate(
    "ARIMA(1,1,1)",
    pred_111
)


# --------------------------------------------------
# 5. ARIMA (2,1,1)
# --------------------------------------------------

arima_211 = ARIMA(
    train["inflation_rate"],
    order=(2, 1, 1)
).fit()

pred_211 = arima_211.forecast(
    len(test)
)

evaluate(
    "ARIMA(2,1,1)",
    pred_211
)


# --------------------------------------------------
# Results
# --------------------------------------------------

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "mae"
).reset_index(drop=True)

print("=" * 70)
print("NIGERIA INFLATION MODEL COMPARISON")
print("=" * 70)
print()

print(
    results_df.round(2).to_string(
        index=False
    )
)

best = results_df.iloc[0]

print()
print(
    f"Best model by MAE: {best['model']}"
)

print(
    f"MAE: {best['mae']:.2f}"
)

print(
    f"RMSE: {best['rmse']:.2f}"
)

results_df.to_csv(
    "reports/inflation_model_comparison.csv",
    index=False
)

print()
print(
    "Model comparison saved successfully!"
)
