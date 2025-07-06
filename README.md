# 📊 DCF Valuation Web App – Python & Streamlit

This project is a professional-grade **Discounted Cash Flow (DCF) Valuation Tool** developed in **Python** with **Streamlit**.  
It provides interactive, real-time company valuation using financial data pulled from Yahoo Finance.

This app is ideal for:

- 💼 Investment Banking (IB)
- 📉 Equity Research
- 🧮 Financial Modeling practice
- 💻 Data-for-Finance projects

---

## 🚀 Live Features

- 📈 DCF valuation with 5-year projected Free Cash Flows (FCF)
- 🔁 Adjustable WACC, FCF growth, and terminal growth rate
- 📊 Enterprise Value & Equity Value computation
- 💰 Fair Value per Share vs. Market Price
- 🧠 Sensitivity analysis (WACC × Terminal Growth)
- 📥 Export of results in Excel format

---

## 🛠️ Tech Stack

- `streamlit` — Web interface  
- `yfinance` — Financial data source  
- `pandas`, `numpy` — Data manipulation  
- `matplotlib`, `seaborn` — Charts & heatmaps  
- `XlsxWriter` — Excel export

---

## 📦 Installation Guide

### 1. Clone this repository

```bash
git clone https://github.com/ludmila-abd/dcf-streamlit-app.git
cd dcf-streamlit-app
```

### 2. Create and activate a virtual environment (optional but recommended)

```bash
python -m venv venv
source venv/bin/activate  # or .\\venv\\Scripts\\activate on Windows
```

### 3. Install the dependencies

Using the provided `requirements.txt`:

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install streamlit yfinance pandas numpy matplotlib seaborn XlsxWriter
```

---

## ▶️ How to Run

```bash
streamlit run app.py
```

This will open the app in your browser at:

```
http://localhost:8501
```

---

## 💡 How It Works

1. You enter a stock ticker (e.g. `AAPL`)
2. The app pulls the company’s financials via `yfinance`
3. It calculates:
   - Free Cash Flow projections (5 years)
   - Discounted cash flows using your selected WACC
   - Terminal Value based on perpetual growth
   - Enterprise Value and Equity Value (adjusted for net debt)
   - Fair Value per Share
4. It then:
   - Compares fair value to live market price
   - Gives a verdict: **UNDERVALUED**, **FAIRLY VALUED**, or **OVERVALUED**
   - Displays a **heatmap** of valuation sensitivity
   - Exports the analysis to an Excel report

---

## 📁 Project Structure

```
deal-screener-valuation/
├── app.py                  # Streamlit application
├── 00_data_test.ipynb      # Raw data exploration (yfinance)
├── 01_screening.ipynb      # Screening multiple stocks by fundamentals
├── 02_valuation.ipynb      # Standalone DCF model in notebook form
├── requirements.txt        # All dependencies
└── README.md               # This documentation
```

---

## 🎯 Ideal Use Cases

- 📊 Students in finance learning DCF modeling
- 🧠 Analysts doing fast valuation checks
- 💻 Python/data science portfolios for IB/PE interviews
- 🧪 Technical case studies in financial engineering

---

## 🔮 To-Do & Next Steps

- [ ] Add downloadable PDF export
- [ ] Deploy on [Streamlit Cloud](https://streamlit.io/cloud)
- [ ] Add peer comparables (P/E, EV/EBITDA)
- [ ] Build multi-ticker valuation dashboard

---

## 👩‍💻 Author

**Ludmila Aboud**  
MSc Applied Math & Finance – Investment Banking Track  
🇫🇷 Paris | 🇺🇸 UCLA | 🇬🇧 Heriot-Watt University  

GitHub: [@ludmila-abd](https://github.com/ludmila-abd)

---

## ⚖️ License

This project is open-source and free to use for learning, academic, and professional demonstration purposes.
