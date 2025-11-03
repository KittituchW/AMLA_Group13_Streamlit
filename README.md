# Crypto Insight – Group 13 (UTS AMLA AT3)

**Repository:** `AMLA_Group13_Streamlit`  
**Deployed App:** [Crypto Insight on Streamlit](https://kittituchw-amla-group13-streamlit-appmain-irplhq.streamlit.app/)

---

## Overview

**Crypto Insight** is an interactive web application for **real-time cryptocurrency forecasting and analysis**, developed as part of the **UTS Advanced Machine Learning Applications (AT3)** project.

The app serves as the **front end** for multiple deployed machine learning models, enabling users to explore **historical market data**, **technical indicators**, and **next-day price predictions** for four cryptocurrencies:
- **Bitcoin (BTC)**
- **Ethereum (ETH)**
- **Solana (SOL)**
- **XRP**

Built with **Streamlit** for simplicity and smooth integration with Python analytics, the app connects directly to **FastAPI endpoints** hosted on **Render**, fetching live data from the **[Kraken OHLC API](https://api.kraken.com/0/public/OHLC)**.

Since the API doesn’t provide technical indicators, the application **computes them locally**, including, **RSI** and **moving averages**, before generating visualizations and model inputs.

---

## Project Structure

The repository is organized to keep the Streamlit web app, API integration, and model files modular and easy to maintain.

```bash
AMLA_GROUP13_STREAMLIT/
│
├── app/ # Main application folder
│ ├── .streamlit/ # Streamlit configuration (theme, layout, etc.)
│ ├── tabs/ # Contains tab pages for Streamlit interface
│ │ ├── ohlc.py # Handles OHLC data and chart visualization
│ │ ├── overview.py # Overview page explaining app purpose
│ │ ├── predictions.py # Tab for displaying real-time predictions
│ │ ├── team.py # Tab showing team members and model metrics
│ │ ├── ui.py # User interface helpers and styling
│ │ └── init.py
│ │
│ ├── data.py # Functions for data retrieval and preprocessing
│ ├── main.py # Main Streamlit entry point
│ └── init.py
│
├── students/ # Individual student model API connections
│ ├── Dylan.py # Connects to Dylan’s CatBoost model API on Render
│ ├── Kittituch.py # Connects to Kittituch’s Linear Regression API on Render
│ ├── Ratticha.py # Connects to Ratticha’s LightGBM API on Render
│ ├── Shawya.py # Connects to Shawya’s XGBoost API on Render
│ └── init.py
│
├── github.txt # Repository and collaboration notes
├── poetry.lock # Poetry dependency lock file
├── pyproject.toml # Project configuration and dependency list
├── requirements.txt # Dependencies list for pip installation
├── runtime.txt # Python version for deployment
└── README.md # Project documentation
```
---

## Main Functionalities

### 1. Interactive Visualization
Displays historical **OHLC** data and calculated indicators such as **RSI** and **moving averages** using **Plotly** charts.  
Users can visually explore price patterns and market trends.

### 2. Real-Time Prediction
Select a cryptocurrency to view the **predicted next-day high price**, generated from the deployed **FastAPI models**.

### 3. Model Performance Dashboard
Compares model performance across all algorithms using key evaluation metrics:  
**RMSE**, **MAE**, **MAPE**, and **R²**.

### 4. Team and Model Overview
Shows each team member’s assigned model along with its performance metrics and project role.

### 5. Data Refresh and Caching
Includes a **refresh button** for updating predictions and cached data with `@st.cache_data`, ensuring fast loading and reduced API calls.

---

## Technology Stack

| Component | Technology |
|------------|-------------|
| **Frontend Framework** | Streamlit |
| **Backend API** | FastAPI (Dockerized and deployed on Render) |
| **Data Source** | Kraken OHLC Public API |
| **Visualization** | Plotly |
| **Model Storage** | Joblib `.pkl` artifacts |
| **Programming Language** | Python 3.11 |
| **Package Management** | `requirements.txt` or Poetry |

---

## Setup and Launch Instructions

### 1. Clone the Repository
```bash
git clone <repository_link>
cd amla_group13_streamlit
```

### 2. Install Dependencies  
Install all required libraries listed in the `requirements.txt` file.  
You can do this by running the command: 

```bash
pip install -r requirements.txt
```

Alternatively, if you are using **Poetry**, run: 

```bash
poetry install
```

### 3. Run the Application Locally  
After installing dependencies, start the Streamlit app by running: 

```bash
streamlit run app/main.py 
```

This will launch the web application in your browser (usually at http://localhost:8501).

### 4. Access the Deployed Version  
You can also access the deployed version directly at:  
[Crypto Insight (Streamlit App)](https://kittituchw-amla-group13-streamlit-appmain-irplhq.streamlit.app/)

The application connects to the **FastAPI model endpoints on Render**, fetching real-time cryptocurrency predictions and displaying model performance metrics.

---


## Team Members

| Member | Model | Description |
|--------|--------|-------------|
| **Kittituch Wongwatcharapaiboon** | Linear Regression | ETH model|
| **Ratticha Ratanawarocha** | LightGBM | XRP model |
| **Shawya Saito** | XGBoost | SOL model |
| **Dylan Jun Jie Leong** | CatBoost | BTC model |


## Project Context

This project was developed for **Assessment Task 3 (AT3)** of **Advanced Machine Learning Applications (36120)** at the **University of Technology Sydney (UTS)**.  
It demonstrates **end-to-end model deployment**, **real-time prediction**, and **interactive visualization** for machine learning in financial markets.