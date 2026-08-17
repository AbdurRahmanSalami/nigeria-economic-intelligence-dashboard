# 🇳🇬 Nigeria Economic Intelligence Dashboard

An interactive data science dashboard for exploring Nigeria's macroeconomic performance, historical trends, economic relationships, and inflation forecasts.

## Live Demo

🌐 [Launch the Nigeria Economic Intelligence Dashboard](https://nigeria-economic-intelligence.streamlit.app)

## Project Overview

This project combines data collection, data engineering, exploratory analysis, statistical modelling, time-series forecasting, and interactive visualisation in a Streamlit application.

Historical Nigerian economic indicators are collected programmatically from the World Bank API, cleaned with Python, combined into a unified dataset, analysed, and presented through an interactive dashboard.

## Features

- World Bank API data collection
- Automated data-cleaning pipeline
- Historical macroeconomic analysis
- Interactive indicator charts
- Custom year-range filtering
- Latest economic indicator cards
- Year-over-year changes
- Executive economic summary
- Correlation analysis
- Interactive relationship explorer
- Inflation forecasting
- Forecast model comparison
- 95% forecast confidence intervals
- Downloadable datasets

## Economic Indicators

The project includes:

- Consumer price inflation
- Official exchange rate
- GDP growth
- Unemployment rate
- Oil rents (% of GDP)
- Foreign reserves
- Current account balance

## Data Sources

Data is collected using the World Bank API for Nigeria (`NGA`).

| Indicator | World Bank Code |
|---|---|
| Inflation | `FP.CPI.TOTL.ZG` |
| Official exchange rate | `PA.NUS.FCRF` |
| GDP growth | `NY.GDP.MKTP.KD.ZG` |
| Unemployment | `SL.UEM.TOTL.ZS` |
| Oil rents | `NY.GDP.PETR.RT.ZS` |
| Total reserves | `FI.RES.TOTL.CD` |
| Current account balance | `BN.CAB.XOKA.GD.ZS` |

## Data Pipeline

World Bank API → Raw JSON → Python Cleaning → Processed CSV → Exploratory Analysis → Forecasting → Streamlit Dashboard

Missing historical observations are retained rather than artificially filled.

## Inflation Forecasting

The following models were evaluated using a 2016–2025 holdout period:

- Naive baseline
- Simple Exponential Smoothing
- Holt damped trend
- ARIMA(1,1,1)
- ARIMA(2,1,1)

The best-performing model was **ARIMA(1,1,1)**.

Backtest performance:

- MAE: 5.51 percentage points
- RMSE: 7.35 percentage points

The selected model was retrained using the complete historical inflation series to generate an experimental 2026–2030 forecast.

## Technology Stack

- Python
- Pandas
- NumPy
- Statsmodels
- Scikit-learn
- Matplotlib
- Plotly
- Streamlit
- World Bank API

## Running Locally

Create and activate a virtual environment:

    python3 -m venv .venv
    source .venv/bin/activate

Install dependencies:

    python -m pip install -r requirements.txt

Launch the application:

    streamlit run dashboard/app.py

## Limitations

- Annual data provides relatively few observations.
- The inflation forecast is univariate.
- Unexpected policy, commodity, food, security, and FX shocks cannot be predicted.
- The unemployment series is a modeled ILO estimate.
- Oil-rents data has shorter recent coverage.
- Correlation does not imply causation.
- Forecasts are experimental and are not official economic projections.

## Purpose

This portfolio project demonstrates practical skills in data collection, data engineering, exploratory data analysis, economic analytics, time-series forecasting, statistical modelling, data visualisation, dashboard development, and analytical communication.
