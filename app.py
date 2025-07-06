# 📊 Streamlit DCF Valuation App with Sensitivity and Export

import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO
from datetime import datetime

st.set_page_config(page_title="DCF Valuation App", layout="centered")
st.title("📈 DCF Valuation Tool")

# === User Inputs ===
ticker = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT):", value="AAPL").upper()
growth_rate = st.slider("Free Cash Flow Growth Rate", 0.00, 0.20, 0.08, step=0.005)
wacc = st.slider("WACC (Discount Rate)", 0.05, 0.15, 0.09, step=0.005)
terminal_growth = st.slider("Terminal Growth Rate", 0.01, 0.05, 0.025, step=0.001)

# === Run analysis ===
if st.button("Run DCF Valuation"):
    stock = yf.Ticker(ticker)
    info = stock.info
    cashflow = stock.cashflow.T
    cols = list(cashflow.columns)

    op_col = next((c for c in cols if "Operating" in c), None)
    capex_col = next((c for c in cols if "Capital Expenditure" in c or "Capital" in c), None)

    if not op_col or not capex_col:
        st.error("❌ FCF data not available.")
    else:
        fcf = (cashflow[op_col] - cashflow[capex_col]).dropna() / 1e9
        fcf.index = fcf.index.astype(str)
        fcf = fcf.sort_index()

        latest_fcf = fcf.iloc[-1]
        projection_years = 5
        fcf_projections = [latest_fcf * (1 + growth_rate) ** i for i in range(1, projection_years + 1)]
        discounted_fcfs = [fcf / ((1 + wacc) ** (i+1)) for i, fcf in enumerate(fcf_projections)]

        terminal_value = fcf_projections[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
        terminal_discounted = terminal_value / ((1 + wacc) ** projection_years)

        enterprise_value = sum(discounted_fcfs) + terminal_discounted
        net_debt = info.get("totalDebt", 0) - info.get("cash", 0)
        equity_value = enterprise_value - net_debt / 1e9
        shares_outstanding = info.get("sharesOutstanding", 1)
        fair_value_per_share = (equity_value * 1e9) / shares_outstanding
        current_price = info.get("currentPrice", 0)

        st.subheader("📊 DCF Valuation Summary")
        st.metric("Fair Value per Share", f"${fair_value_per_share:.2f}")
        st.metric("Current Price", f"${current_price:.2f}")

        # === FCF Chart ===
        fcf_df = pd.DataFrame({
            "Projected FCF": fcf_projections,
            "Discounted FCF": discounted_fcfs
        }, index=[f"Year {i}" for i in range(1, projection_years + 1)])

        st.subheader("💵 Free Cash Flow Projection")
        st.dataframe(fcf_df)
        fig, ax = plt.subplots()
        fcf_df.plot(kind="bar", ax=ax)
        plt.title(f"{ticker} – FCF Projections")
        plt.ylabel("Billion USD")
        st.pyplot(fig)

        # === Sensitivity Analysis ===
        st.subheader("🧠 Sensitivity Analysis (Fair Value per Share)")
        wacc_range = [wacc - 0.01, wacc, wacc + 0.01]
        growth_range = [terminal_growth - 0.005, terminal_growth, terminal_growth + 0.005]

        sens_df = pd.DataFrame(index=[f"{w*100:.1f}%" for w in wacc_range],
                               columns=[f"{g*100:.2f}%" for g in growth_range])

        for w in wacc_range:
            for g in growth_range:
                tv = fcf_projections[-1] * (1 + g) / (w - g)
                tv_disc = tv / ((1 + w) ** projection_years)
                fcfs_disc = [f / ((1 + w) ** (i+1)) for i, f in enumerate(fcf_projections)]
                ev = sum(fcfs_disc) + tv_disc
                eq = ev - net_debt / 1e9
                fair_val = (eq * 1e9) / shares_outstanding
                sens_df.loc[f"{w*100:.1f}%", f"{g*100:.2f}%"] = round(fair_val, 2)

        st.dataframe(sens_df)
        fig2, ax2 = plt.subplots()
        sns.heatmap(sens_df.astype(float), annot=True, fmt=".1f", cmap="YlGnBu", ax=ax2)
        plt.title(f"{ticker} – DCF Sensitivity Analysis")
        st.pyplot(fig2)

        # === Export to Excel ===
        st.subheader("📤 Export Results")
        output = BytesIO()
        with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
            pd.DataFrame({"Historical FCF (B USD)": fcf}).to_excel(writer, sheet_name="Historical FCF")
            fcf_df.to_excel(writer, sheet_name="Projection")
            sens_df.to_excel(writer, sheet_name="Sensitivity")
            pd.DataFrame({"Fair Value per Share": [fair_value_per_share],
                          "Current Price": [current_price]}).to_excel(writer, sheet_name="Summary")
          
        st.download_button(
            label="📥 Download Excel Report",
            data=output.getvalue(),
            file_name=f"{ticker}_DCF_Valuation.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
