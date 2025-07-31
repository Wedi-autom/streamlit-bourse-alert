import yfinance as yf
import streamlit as st

st.title("📉 Veille boursière : pharma EU & US")

tickers = ['CLARI.PA', 'VLA.PA', 'SNY']  # ajoute d'autres tickers si souhaité
seuil = st.slider("Seuil chute (%) pour alerte :", 1, 10, 3)

for ticker in tickers:
    df = yf.download(ticker, period='1d', interval='5m')
    if df.empty:
        st.warning(f"Aucune donnée pour {ticker}")
        continue
    open_price = df['Open'].iloc[0]
    last_price = df['Close'].iloc[-1]
    drop = (open_price - last_price) / open_price * 100
    st.subheader(ticker)
    st.write(f"Ouverture : {open_price:.2f} — Dernier : {last_price:.2f}")
    st.write(f"Chute depuis ouverture : {drop:.2f}%")
    if drop >= seuil:
        st.error(f"⚠️ Alerte : {ticker} chute de {drop:.2f}% aujourd'hui !")
