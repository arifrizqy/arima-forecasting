import mysql.connector
import streamlit as st
import pandas as pd
import numpy as np
import datetime
import plotly.express as px
import plotly.graph_objects as go
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.stattools import adfuller, acf, pacf

def connect_to_db():
	return mysql.connector.connect(
		host="localhost",
		user="arifrizqy",
		password="@Arriz2401",
		database="forecasting_db"
	)

def fetch_data():
	conn = connect_to_db()
	query = "SELECT date, value FROM forecast_data"
	data = pd.read_sql(query, conn)
	conn.close()
	return data

def check_stationarity(data):
  return adfuller(data)

st.set_page_config(page_title="ARIMA Forecasting", layout="wide")
st.title("Aplikasi Forecasting Data Metode ARIMA (AutoRegresive Integrated Moving Average)")

if "p_val" not in st.session_state:
    st.session_state.p_val = 0  # Nilai default P
if "d_val" not in st.session_state:
    st.session_state.d_val = 0  # Nilai default D
if "q_val" not in st.session_state:
    st.session_state.q_val = 0  # Nilai default Q

tab1, tab2, tab3 = st.tabs(["Perumusan Model", "Forecasting", "About"])

with tab1:
	st.header("Perumusan Model")

	col1, col2 = st.columns([1, 3])
	with col1:
		st.subheader("Data Actual")
		data = fetch_data()
		st.dataframe(data)
  
	with col2:
		st.subheader("Form Data")

		with st.form(key="form1"):
			col21, col22 = st.columns([1, 1])
			with col21:
				date = st.date_input("Pilih tanggal:")

			with col22:
				value = st.number_input("Masukkan nilai actual:")

			store_to_db = st.form_submit_button("Simpan Data")

		st.subheader("Plot Data Actual")
		st.line_chart(data.set_index("date")["value"])

		res = check_stationarity(data['value'])
  
		col23, col24 = st.columns([1, 1.5])
		with col23:
			st.write(f"P-Value : {res[1]:.10f}")
			st.write(f"Differencing : {st.session_state.d_val}")
  
		with col24:
			if res[1] > 0.05:
				st.warning("Data belum stationer")
			else:
				st.success("Data stationer")

	if res[1] > 0.05:
		st.subheader("Stationeritas")
		diff_data = data["value"].diff().dropna()
		if st.button("Stationerkan sampai optimal"):
			while res[1] > 0.05:
				st.session_state.d_val += 1
				res = check_stationarity(diff_data)
			
			col3, col4 = st.columns([1, 2.5])
			with col3:
				st.write(f"P-Value : {res[1]:.10f}")
				st.write(f"Differencing : {st.session_state.d_val}")

			with col4:
				if res[1] > 0.05:
					st.warning("Data belum stationer")
				else:
					st.success("Data stationer")

			st.line_chart(diff_data)

	st.subheader("Plot ACF dan PACF")
	# Hitung nilai ACF dan PACF
	acf_values = acf(data["value"].dropna(), fft=False, nlags=20)
	pacf_values = pacf(data["value"].dropna(), nlags=20)

	# Plot ACF menggunakan garis dengan spike
	fig_acf = go.Figure()
	fig_acf.add_trace(go.Scatter(x=list(range(len(acf_values))),
															y=acf_values,
															mode="lines+markers",
															name="ACF"))
	for i in range(len(acf_values)):
			fig_acf.add_trace(go.Scatter(x=[i, i], y=[0, acf_values[i]], mode="lines", line=dict(color="blue", width=1)))

	fig_acf.update_layout(title="Autocorrelation Function (ACF)",
												xaxis_title="Lag",
												yaxis_title="Correlation",
												showlegend=False)

	# Plot PACF menggunakan garis dengan spike
	fig_pacf = go.Figure()
	fig_pacf.add_trace(go.Scatter(x=list(range(len(pacf_values))),
																y=pacf_values,
																mode="lines+markers",
																name="PACF"))
	for i in range(len(pacf_values)):
			fig_pacf.add_trace(go.Scatter(x=[i, i], y=[0, pacf_values[i]], mode="lines", line=dict(color="blue", width=1)))

	fig_pacf.update_layout(title="Partial Autocorrelation Function (PACF)",
												xaxis_title="Lag",
												yaxis_title="Correlation",
												showlegend=False)

	# Tampilkan di Streamlit
	col5, col6 = st.columns([1, 1])
	with col5:
		st.plotly_chart(fig_acf)
	with col6:
		st.plotly_chart(fig_pacf)

	st.markdown("""
### Tips:
Untuk memilih nilai p dan q dari plot ACF dan PACF diatas untuk pemodelan ARIMA(p, d, q)
- Nilai q dapat ditentukan dengan cara memeriksa lag tempat ACF pertama kali memotong garis nol.
- Nilai p dapat ditentukan dengan cara memeriksa lag tempat PACF pertama kali memotong garis nol.
""")

with tab2:
	st.header("Forecasting")

	col7, col8 = st.columns([1, 2])
	with col7:
		st.session_state.p_val = int(st.number_input(
        "Masukkan nilai untuk parameter P:",
        min_value=0,
        step=1,
        value=st.session_state.p_val,
        key="p_input"
    ))
  
		st.session_state.d_val = int(st.number_input(
        "Masukkan nilai untuk parameter D:",
        min_value=0,
        step=1,
        value=st.session_state.d_val,
        key="d_input"
    ))
  
		st.session_state.q_val = int(st.number_input(
        "Masukkan nilai untuk parameter Q:",
        min_value=0,
        step=1,
        value=st.session_state.q_val,
        key="q_input"
    ))

		calculate = st.button("Hitung")
	with col8:
		if calculate:
			model = ARIMA(data["value"], order=(st.session_state.p_val, st.session_state.d_val, st.session_state.q_val))
			fit_model = model.fit()

			st.write(fit_model.summary())

			forecast = fit_model.forecast(steps=12)
			st.line_chart(forecast)
			predict = fit_model.predict()

			df_plot = pd.DataFrame({
				"Date": data['date'],
				"Actual": data['value'],
				"Predict": predict
			})

			fig = px.line(
				df_plot,
				x="Date",
				y=["Actual", "Predict"],
				labels={"value": "Values", "Date": "Date"},
				title="Plot Actual vs Predict"
			)

			st.plotly_chart(fig)