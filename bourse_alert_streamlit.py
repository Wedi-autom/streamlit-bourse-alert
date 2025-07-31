import yfinance as yf
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Alerte Boursière IA", layout="wide")

st.title("📉 Alerte de Chute Boursière")

# Liste d'actions suivies
tickers = st.multiselect("Sélectionnez les actions à suivre :", ['ENR1n', 'MSFT', 'NVDA', 'TSLA', 'AMZN', 'GOOGL'], default=['AAPL', 'MSFT'])
seuil = st.slider("Seuil de chute (%) pour alerte :", 1, 10, 3)

if st.button("🔍 Lancer l'analyse"):
    alertes = []
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    for ticker in tickers:
        df = yf.download(ticker, period='1d', interval='5m')
        if df.empty:
            st.warning(f"⛔ Données indisponibles pour {ticker}")
            continue

        open_price = df['Open'].iloc[0]
        close_price = df['Close'].iloc[-1]
        drop_percent = (open_price - close_price) / open_price * 100

        col1, col2 = st.columns([2, 1])
        with col1:
            st.subheader(f"{ticker}")
            st.line_chart(df['Close'])
        with col2:
            st.metric(label="Ouverture", value=f"{open_price:.2f}")
            st.metric(label="Dernier prix", value=f"{close_price:.2f}")
            st.metric(label="Chute (%)", value=f"{drop_percent:.2f}%", delta=f"{-drop_percent:.2f}%")

        if drop_percent >= seuil:
            alertes.append(f"⚠️ {ticker} a chuté de {drop_percent:.2f}% !")

    if alertes:
        st.error("\n".join(alertes))
    else:
        st.success(f"Aucune alerte détectée à {now}.")
