from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Nigeria Economic Intelligence Dashboard",
    page_icon="🇳🇬",
    layout="wide"
)

BASE_DIR = Path(__file__).resolve().parents[1]

DATA_FILE = (
    BASE_DIR /
    "data/processed/nigeria_economic_data.csv"
)

FORECAST_FILE = (
    BASE_DIR /
    "reports/inflation_forecast_2026_2030.csv"
)

MODEL_FILE = (
    BASE_DIR /
    "reports/inflation_model_comparison.csv"
)


# ============================================================
# STYLING
# ============================================================

st.markdown(
    """
    <style>

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        max-width: 1450px;
    }

    [data-testid="stMetric"] {
        border: 1px solid rgba(128,128,128,0.18);
        border-radius: 12px;
        padding: 18px;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
    }

    div[data-testid="stAlert"] {
        border-radius: 10px;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    economic_data = pd.read_csv(
        DATA_FILE
    )

    forecast_data = pd.read_csv(
        FORECAST_FILE
    )

    if MODEL_FILE.exists():
        model_data = pd.read_csv(
            MODEL_FILE
        )
    else:
        model_data = None

    return (
        economic_data,
        forecast_data,
        model_data
    )


df, forecast_df, model_df = load_data()


# ============================================================
# HELPERS
# ============================================================

def get_latest(column):

    data = (
        df[["year", column]]
        .dropna()
        .sort_values("year")
    )

    latest = data.iloc[-1]

    previous = (
        data.iloc[-2]
        if len(data) > 1
        else latest
    )

    return {
        "year": int(latest["year"]),
        "value": float(latest[column]),
        "previous_year": int(previous["year"]),
        "previous_value": float(previous[column])
    }


def format_change(
    current,
    previous,
    suffix=""
):

    change = current - previous

    return f"{change:+.2f}{suffix}"


# ============================================================
# HEADER
# ============================================================

st.title(
    "🇳🇬 Nigeria Economic Intelligence Dashboard"
)

st.markdown(
    """
    An interactive data-science platform for exploring
    **Nigeria's macroeconomic performance, historical trends,
    economic relationships and inflation forecasts**.
    """
)

st.caption(
    "Historical data: World Bank API • "
    "Forecasting: ARIMA • "
    "Coverage: 1960–2025"
)

st.divider()


# ============================================================
# NAVIGATION
# ============================================================

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Overview",
        "Historical Trends",
        "Inflation Forecast",
        "Economic Relationships",
        "Methodology & Data"
    ]
)


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with tab1:

    st.subheader(
        "Latest Economic Indicators"
    )

    inflation = get_latest(
        "inflation_rate"
    )

    exchange = get_latest(
        "exchange_rate"
    )

    gdp = get_latest(
        "gdp_growth"
    )

    unemployment = get_latest(
        "unemployment_rate"
    )

    reserves = get_latest(
        "reserves_usd_billion"
    )

    current_account = get_latest(
        "current_account_pct_gdp"
    )


    # -------------------------------
    # ROW 1
    # -------------------------------

    col1, col2, col3 = st.columns(3)

    col1.metric(
        label=f"Inflation ({inflation['year']})",
        value=f"{inflation['value']:.2f}%",
        delta=format_change(
            inflation["value"],
            inflation["previous_value"],
            " pp"
        ),
        delta_color="inverse"
    )


    fx_change_pct = (
        (
            exchange["value"] /
            exchange["previous_value"]
        ) - 1
    ) * 100

    col2.metric(
        label=(
            f"Official Exchange Rate "
            f"({exchange['year']})"
        ),
        value=f"₦{exchange['value']:,.2f}/$",
        delta=f"{fx_change_pct:+.2f}%",
        delta_color="inverse"
    )


    col3.metric(
        label=f"GDP Growth ({gdp['year']})",
        value=f"{gdp['value']:.2f}%",
        delta=format_change(
            gdp["value"],
            gdp["previous_value"],
            " pp"
        )
    )


    # -------------------------------
    # ROW 2
    # -------------------------------

    col4, col5, col6 = st.columns(3)

    col4.metric(
        label=(
            f"Unemployment "
            f"({unemployment['year']})"
        ),
        value=f"{unemployment['value']:.2f}%",
        delta=format_change(
            unemployment["value"],
            unemployment["previous_value"],
            " pp"
        ),
        delta_color="inverse"
    )


    col5.metric(
        label=(
            f"Foreign Reserves "
            f"({reserves['year']})"
        ),
        value=f"${reserves['value']:.2f}B",
        delta=format_change(
            reserves["value"],
            reserves["previous_value"],
            "B"
        )
    )


    col6.metric(
        label=(
            f"Current Account "
            f"({current_account['year']})"
        ),
        value=(
            f"{current_account['value']:.2f}% "
            "of GDP"
        ),
        delta=format_change(
            current_account["value"],
            current_account["previous_value"],
            " pp"
        )
    )


    # -------------------------------
    # EXECUTIVE SUMMARY
    # -------------------------------

    st.divider()

    st.subheader(
        "Executive Economic Snapshot"
    )

    inflation_change = (
        inflation["value"] -
        inflation["previous_value"]
    )

    gdp_change = (
        gdp["value"] -
        gdp["previous_value"]
    )

    reserves_change = (
        reserves["value"] -
        reserves["previous_value"]
    )

    insight1 = (
        "Inflation eased by "
        f"{abs(inflation_change):.2f} percentage points "
        f"from {inflation['previous_year']}."
        if inflation_change < 0
        else
        "Inflation increased by "
        f"{inflation_change:.2f} percentage points "
        f"from {inflation['previous_year']}."
    )

    insight2 = (
        "The official annual-average naira exchange rate "
        f"changed by {fx_change_pct:+.2f}% relative to "
        f"{exchange['previous_year']}."
    )

    insight3 = (
        f"GDP growth changed by {gdp_change:+.2f} "
        f"percentage points from {gdp['previous_year']}."
    )

    insight4 = (
        f"Foreign reserves changed by "
        f"${reserves_change:+.2f}B from "
        f"{reserves['previous_year']}."
    )

    st.markdown(
        f"""
        - **Inflation:** {insight1}
        - **Foreign exchange:** {insight2}
        - **Economic growth:** {insight3}
        - **External buffers:** {insight4}
        """
    )


    # -------------------------------
    # RECENT SNAPSHOT
    # -------------------------------

    st.divider()

    st.subheader(
        "Recent Economic Performance"
    )

    recent = df[
        df["year"] >= 2015
    ].copy()

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=recent["year"],
            y=recent["inflation_rate"],
            mode="lines+markers",
            name="Inflation (%)"
        )
    )

    fig.add_trace(
        go.Scatter(
            x=recent["year"],
            y=recent["gdp_growth"],
            mode="lines+markers",
            name="GDP Growth (%)"
        )
    )

    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Percent",
        hovermode="x unified",
        legend_title_text=""
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# TAB 2 — HISTORICAL TRENDS
# ============================================================

with tab2:

    st.subheader(
        "Historical Indicator Explorer"
    )

    indicators = {

        "Inflation Rate": (
            "inflation_rate",
            "%"
        ),

        "Official Exchange Rate": (
            "exchange_rate",
            "₦ per US$"
        ),

        "GDP Growth": (
            "gdp_growth",
            "%"
        ),

        "Unemployment Rate": (
            "unemployment_rate",
            "%"
        ),

        "Oil Rents": (
            "oil_rents_pct_gdp",
            "% of GDP"
        ),

        "Foreign Reserves": (
            "reserves_usd_billion",
            "US$ Billion"
        ),

        "Current Account Balance": (
            "current_account_pct_gdp",
            "% of GDP"
        )
    }


    selected_indicator = st.selectbox(
        "Select an economic indicator",
        list(indicators.keys())
    )

    column, unit = indicators[
        selected_indicator
    ]

    chart_data = (
        df[["year", column]]
        .dropna()
        .sort_values("year")
    )

    minimum_year = int(
        chart_data["year"].min()
    )

    maximum_year = int(
        chart_data["year"].max()
    )

    default_start = max(
        minimum_year,
        maximum_year - 25
    )


    year_range = st.slider(
        "Select year range",
        min_value=minimum_year,
        max_value=maximum_year,
        value=(
            default_start,
            maximum_year
        )
    )


    filtered = chart_data[
        (
            chart_data["year"] >=
            year_range[0]
        ) &
        (
            chart_data["year"] <=
            year_range[1]
        )
    ]


    fig = px.line(
        filtered,
        x="year",
        y=column,
        markers=True,
        title=(
            f"Nigeria: {selected_indicator} "
            f"({year_range[0]}–{year_range[1]})"
        )
    )


    if (
        filtered[column].min() < 0 <
        filtered[column].max()
    ):

        fig.add_hline(
            y=0,
            line_dash="dash"
        )


    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=unit,
        hovermode="x unified"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -------------------------------
    # SUMMARY STATISTICS
    # -------------------------------

    latest_row = filtered.iloc[-1]

    average_value = filtered[
        column
    ].mean()

    maximum_row = filtered.loc[
        filtered[column].idxmax()
    ]

    minimum_row = filtered.loc[
        filtered[column].idxmin()
    ]


    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Latest",
        f"{latest_row[column]:,.2f} {unit}"
    )

    c2.metric(
        "Period Average",
        f"{average_value:,.2f} {unit}"
    )

    c3.metric(
        f"Peak ({int(maximum_row['year'])})",
        f"{maximum_row[column]:,.2f} {unit}"
    )

    c4.metric(
        f"Low ({int(minimum_row['year'])})",
        f"{minimum_row[column]:,.2f} {unit}"
    )


# ============================================================
# TAB 3 — FORECASTING
# ============================================================

with tab3:

    st.subheader(
        "Inflation Forecast: 2026–2030"
    )

    st.warning(
        """
        This is an experimental statistical forecast,
        not an official economic projection. Forecast
        uncertainty increases significantly over longer
        horizons.
        """
    )


    history = (
        df[
            ["year", "inflation_rate"]
        ]
        .dropna()
    )

    history = history[
        history["year"] >= 1990
    ]


    fig = go.Figure()


    fig.add_trace(
        go.Scatter(
            x=history["year"],
            y=history["inflation_rate"],
            mode="lines+markers",
            name="Historical Inflation"
        )
    )


    fig.add_trace(
        go.Scatter(
            x=forecast_df["year"],
            y=forecast_df[
                "forecast_inflation"
            ],
            mode="lines+markers",
            name="ARIMA Forecast",
            line=dict(
                dash="dash"
            )
        )
    )


    fig.add_trace(
        go.Scatter(
            x=forecast_df["year"],
            y=forecast_df["upper_95"],
            mode="lines",
            line=dict(width=0),
            showlegend=False
        )
    )


    fig.add_trace(
        go.Scatter(
            x=forecast_df["year"],
            y=forecast_df["lower_95"],
            mode="lines",
            line=dict(width=0),
            fill="tonexty",
            name="95% Confidence Interval"
        )
    )


    fig.add_vline(
        x=2025,
        line_dash="dash"
    )


    fig.update_layout(
        xaxis_title="Year",
        yaxis_title="Inflation Rate (%)",
        hovermode="x unified"
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    forecast_2026 = forecast_df.iloc[0]
    forecast_2030 = forecast_df.iloc[-1]

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "2026 Forecast",
        f"{forecast_2026['forecast_inflation']:.2f}%"
    )

    c2.metric(
        "2030 Forecast",
        f"{forecast_2030['forecast_inflation']:.2f}%"
    )

    c3.metric(
        "Change: 2026 → 2030",
        (
            f"{forecast_2030['forecast_inflation'] - forecast_2026['forecast_inflation']:+.2f} pp"
        )
    )


    st.subheader(
        "Forecast Values"
    )


    display_forecast = (
        forecast_df.copy()
    )

    display_forecast.columns = [
        "Year",
        "Forecast Inflation (%)",
        "Lower 95% (%)",
        "Upper 95% (%)"
    ]


    st.dataframe(
        display_forecast,
        use_container_width=True,
        hide_index=True
    )


    st.caption(
        """
        Negative lower confidence bounds do not mean
        that the model specifically predicts deflation.
        They reflect the high statistical uncertainty
        of long-range forecasts using annual data.
        """
    )


    if model_df is not None:

        st.divider()

        st.subheader(
            "Model Evaluation"
        )

        st.markdown(
            """
            Forecasting models were evaluated on an
            unseen **2016–2025 holdout period**.
            Lower MAE and RMSE indicate better predictive
            performance.
            """
        )

        model_display = (
            model_df
            .sort_values("mae")
            .copy()
        )

        model_display.columns = [
            "Model",
            "MAE",
            "RMSE"
        ]

        st.dataframe(
            model_display.round(2),
            use_container_width=True,
            hide_index=True
        )

        best_model = model_display.iloc[0]

        st.success(
            f"Best backtest model: "
            f"{best_model['Model']} — "
            f"MAE {best_model['MAE']:.2f}, "
            f"RMSE {best_model['RMSE']:.2f}"
        )


# ============================================================
# TAB 4 — RELATIONSHIPS
# ============================================================

with tab4:

    st.subheader(
        "Economic Relationships"
    )

    st.markdown(
        """
        This section examines linear relationships between
        indicators during the **1991–2021 common period**.

        Exchange rates and reserves are represented by their
        annual percentage changes rather than raw levels.
        """
    )


    # IMPORTANT:
    # Calculate percentage changes BEFORE slicing dates.

    relationship_df = df.copy()

    relationship_df[
        "FX Change"
    ] = (
        relationship_df[
            "exchange_rate"
        ].pct_change() * 100
    )

    relationship_df[
        "Reserves Change"
    ] = (
        relationship_df[
            "reserves_usd_billion"
        ].pct_change() * 100
    )


    relationship_df = relationship_df[
        (
            relationship_df["year"] >= 1991
        ) &
        (
            relationship_df["year"] <= 2021
        )
    ].copy()


    columns = {
        "Inflation":
            "inflation_rate",

        "FX Change":
            "FX Change",

        "GDP Growth":
            "gdp_growth",

        "Unemployment":
            "unemployment_rate",

        "Oil Rents":
            "oil_rents_pct_gdp",

        "Reserves Change":
            "Reserves Change",

        "Current Account":
            "current_account_pct_gdp"
    }


    correlation_data = (
        relationship_df[
            list(columns.values())
        ]
        .dropna()
    )


    correlation = (
        correlation_data
        .corr()
    )

    correlation.columns = (
        list(columns.keys())
    )

    correlation.index = (
        list(columns.keys())
    )


    fig = go.Figure(
        data=go.Heatmap(
            z=correlation.values,
            x=correlation.columns,
            y=correlation.index,
            zmin=-1,
            zmax=1,
            zmid=0,
            text=correlation.round(2).values,
            texttemplate="%{text}",
            colorbar=dict(
                title="Correlation"
            )
        )
    )


    fig.update_layout(
        title=(
            "Nigeria Economic Correlations, "
            "1991–2021"
        )
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    # -------------------------------
    # DYNAMIC STRONGEST RELATIONSHIPS
    # -------------------------------

    pairs = []

    labels = list(
        correlation.columns
    )

    for i in range(len(labels)):

        for j in range(
            i + 1,
            len(labels)
        ):

            value = correlation.iloc[
                i, j
            ]

            pairs.append(
                (
                    labels[i],
                    labels[j],
                    value
                )
            )


    strongest = sorted(
        pairs,
        key=lambda x: abs(x[2]),
        reverse=True
    )[:5]


    st.subheader(
        "Strongest Historical Relationships"
    )


    for left, right, value in strongest:

        direction = (
            "positive"
            if value > 0
            else "negative"
        )

        st.markdown(
            f"- **{left} ↔ {right}: "
            f"{value:+.2f}** "
            f"({direction} correlation)"
        )


    st.caption(
        """
        Correlation describes statistical association.
        It does not establish that one economic variable
        causes another.
        """
    )


    # -------------------------------
    # RELATIONSHIP EXPLORER
    # -------------------------------

    st.divider()

    st.subheader(
        "Relationship Explorer"
    )

    c1, c2 = st.columns(2)

    x_label = c1.selectbox(
        "X-axis indicator",
        labels,
        index=0
    )

    y_label = c2.selectbox(
        "Y-axis indicator",
        labels,
        index=2
    )


    x_column = columns[x_label]
    y_column = columns[y_label]


    scatter_data = relationship_df[
        [
            "year",
            x_column,
            y_column
        ]
    ].dropna()


    fig = px.scatter(
        scatter_data,
        x=x_column,
        y=y_column,
        hover_data=["year"],
        trendline="ols",
        title=(
            f"{x_label} vs {y_label}"
        )
    )


    fig.update_layout(
        xaxis_title=x_label,
        yaxis_title=y_label
    )


    st.plotly_chart(
        fig,
        use_container_width=True
    )


    pair_corr = (
        scatter_data[
            [x_column, y_column]
        ]
        .corr()
        .iloc[0, 1]
    )


    st.info(
        f"Correlation between {x_label} and "
        f"{y_label}: {pair_corr:+.2f}"
    )


# ============================================================
# TAB 5 — METHODOLOGY AND DATA
# ============================================================

with tab5:

    st.subheader(
        "Data Sources & Methodology"
    )

    st.markdown(
        """
        ### Data source

        Historical indicators were collected programmatically
        using the **World Bank API** for Nigeria (`NGA`).

        | Indicator | World Bank code |
        |---|---|
        | Inflation, consumer prices | `FP.CPI.TOTL.ZG` |
        | Official exchange rate | `PA.NUS.FCRF` |
        | GDP growth | `NY.GDP.MKTP.KD.ZG` |
        | Unemployment, modeled ILO estimate | `SL.UEM.TOTL.ZS` |
        | Oil rents (% of GDP) | `NY.GDP.PETR.RT.ZS` |
        | Total reserves | `FI.RES.TOTL.CD` |
        | Current account balance (% GDP) | `BN.CAB.XOKA.GD.ZS` |

        ### Data engineering pipeline

        **World Bank API → Raw JSON → Python cleaning →
        Processed CSV → Statistical analysis → Streamlit dashboard**

        Missing observations are preserved as missing rather
        than being artificially imputed.

        ### Forecasting

        Multiple forecasting methods were evaluated using an
        unseen **2016–2025 test period**.

        The best-performing model was **ARIMA(1,1,1)**.

        The final model was retrained on the complete inflation
        series and used to generate an experimental 2026–2030
        forecast.

        ### Important limitations

        - Annual data provides relatively few observations.
        - The forecast is univariate.
        - Structural economic reforms cannot be known in advance.
        - Commodity, food, security and policy shocks may alter outcomes.
        - The unemployment series is a modeled ILO estimate.
        - Oil-rents data has shorter recent coverage than most indicators.
        - Correlation does not imply causation.
        """
    )


    st.divider()

    st.subheader(
        "Download Project Data"
    )


    master_csv = df.to_csv(
        index=False
    ).encode("utf-8")


    forecast_csv = (
        forecast_df
        .to_csv(index=False)
        .encode("utf-8")
    )


    c1, c2 = st.columns(2)


    c1.download_button(
        label="Download Economic Dataset",
        data=master_csv,
        file_name=(
            "nigeria_economic_data.csv"
        ),
        mime="text/csv"
    )


    c2.download_button(
        label="Download Inflation Forecast",
        data=forecast_csv,
        file_name=(
            "nigeria_inflation_forecast.csv"
        ),
        mime="text/csv"
    )
