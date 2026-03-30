# 📊 PhonePe Pulse Data Analysis

An end-to-end data analysis and visualization project built using **PhonePe Pulse open data**. This project analyzes large-scale digital transaction data to extract meaningful insights on **user behavior, transaction patterns, insurance adoption, and regional growth trends across India**.

---

## 🛠️ Tech Stack

- **Python** — Data extraction, transformation, and analysis
- **PostgreSQL** — Relational database for structured data storage
- **SQLAlchemy** — Database connectivity
- **Pandas** — Data manipulation and cleaning
- **Plotly** — Interactive data visualizations
- **Streamlit** — Interactive web dashboard

---

## 📁 Project Structure

```
PhonePe/
├── phonepe_ana.ipynb    # Data extraction, cleaning, SQL analysis & insights
├── app.py           # Streamlit dashboard application
├── requirements.txt     # Python dependencies
├── README.md            # Project documentation
└── .gitignore
```

---

## 🗄️ Database Schema

Data is organized into **9 tables** across 3 categories:

| Category | Table | Description |
|----------|-------|-------------|
| Aggregated | `agg_trans` | Transaction data by state, year, quarter, type |
| Aggregated | `agg_ins` | Insurance transaction data |
| Aggregated | `agg_user` | User registration and app usage data |
| Map | `map_trans` | District-level transaction mapping |
| Map | `map_ins` | District-level insurance mapping |
| Map | `map_user_list` | District-level user registration data |
| Top | `top_trans` | Top states/districts by transactions |
| Top | `top_ins` | Top states/districts by insurance |
| Top | `top_user_list` | Top states/districts by users |

---

## 📊 Business Case Studies

The dashboard covers **5 real-world business scenarios**:

### 1. Decoding Transaction Dynamics
- Choropleth map of India showing state-wise transaction values
- Payment method popularity (pie charts)
- Top 10 states by transaction amount
- Transaction composition (stacked bar) and trend analysis

### 2. Insurance Penetration & Growth
- Top states by insurance transactions
- Quarter-wise and year-wise growth trends
- State-level insurance trend analysis

### 3. User Engagement & Growth
- Top states by engagement (bar chart)
- Year-over-year growth (line plot)
- Engagement by transaction type (stacked area)
- Engagement vs transaction value (scatter plot)

### 4. Insurance Engagement
- State-wise insurance engagement rankings
- Year-wise and quarter-wise engagement trends

### 5. User Registration Analysis
- Top states by user registrations
- Registration growth over time
- State-level registration trends

---

## 🔑 Key Insights

- **Maharashtra, Karnataka, and Telangana** consistently lead in transaction volume and value
- **Peer-to-peer payments** dominate, accounting for the largest share of transaction amount
- **Insurance adoption has grown significantly** from 2020 to 2024, with Q4 showing peak activity each year
- **Recharge & bill payments** have the highest transaction count but lower average transaction value
- **Southern and western states** show higher engagement ratios relative to registered users

---

## ⚙️ Setup & Installation

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up PostgreSQL
- Create a database named `phonepe_data` in PostgreSQL
- Set the environment variable with your connection URL:
```powershell
# Windows PowerShell
[System.Environment]::SetEnvironmentVariable("PHONEPE_DB_URL", "postgresql+psycopg://postgres:YOUR_PASSWORD@127.0.0.1:5432/phonepe_data", "User")
```

### 3. Run the notebook
- Open `trial.ipynb` and run all cells to extract, clean, and load data into PostgreSQL

### 4. Launch the dashboard
```bash
streamlit run st_phnp.py
```

---

## 📈 Visualization Types Used

- Choropleth Maps (India state-level)
- Bar Charts & Stacked Bar Charts
- Pie / Donut Charts
- Line Plots
- Stacked Area Plots
- Scatter Plots

---

## 📝 Data Source

This project uses publicly available data from the [PhonePe Pulse GitHub Repository](https://github.com/PhonePe/pulse).


