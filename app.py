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
	query = "SELECT id, date, value FROM forecast_data"
	data = pd.read_sql(query, conn)
	conn.close()
	return data

def insert_data(date, value):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = "INSERT INTO forecast_data (date, value) VALUES (%s, %s)"
        cursor.execute(query, (date, value))
        connection.commit()
        st.success("Data berhasil disimpan!")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
    finally:
        cursor.close()
        connection.close()

def del_data(id):
    connection = connect_to_db()
    cursor = connection.cursor()
    try:
        query = f"DELETE from forecast_data WHERE id={id}"
        cursor.execute(query)
        connection.commit()
        st.success("Data berhasil dihapus!")
    except Exception as e:
        st.error(f"Terjadi kesalahan: {e}")
    finally:
        cursor.close()
        connection.close()

def check_stationarity(data):
  return adfuller(data)

def calculate_mape(actual, predict):
    actual = np.array(actual)
    predict = np.array(predict)
    non_zero_actual = actual != 0
    mape = np.mean(np.abs((actual[non_zero_actual] - predict[non_zero_actual]) / actual[non_zero_actual])) * 100
    return mape

st.set_page_config(page_title="ARIMA Forecasting", layout="wide")
st.title("Aplikasi Forecasting Data Metode ARIMA (AutoRegresive Integrated Moving Average)")

p_val = 0
d_val = 0
q_val = 0

tab1, tab2, tab3 = st.tabs(["Perumusan Model", "Forecasting", "About"])

with tab1:
	st.header("Perumusan Model")

	col1, col2 = st.columns([1, 3])
	with col1:
		st.subheader("Data Actual")
		data = fetch_data()
		st.write(data)
  
		with st.form(key="form_del"):
			id = int(st.number_input("Masukkan ID data yang akan dihapus", min_value=0, step=1))
			del_btn = st.form_submit_button("Hapus Data")

			if del_btn:
				del_data(id)
  
	with col2:
		st.subheader("Form Data")

		with st.form(key="form1"):
			col21, col22 = st.columns([1, 1])
			with col21:
				date = st.date_input("Pilih tanggal:")

			with col22:
				value = st.number_input("Masukkan nilai actual:", min_value=0, step=1)

			store_to_db = st.form_submit_button("Simpan Data")
			if store_to_db:
				insert_data(date, value)

		st.subheader("Plot Data Actual")
		st.line_chart(data.set_index("date")["value"])

		res = check_stationarity(data['value'])
  
		col23, col24 = st.columns([1, 1.5])
		with col23:
			st.write(f"P-Value : {res[1]:.10f}")
			st.write(f"Differencing : {d_val}")
  
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
				d_val += 1
				res = check_stationarity(diff_data)
			
			col3, col4 = st.columns([1, 2.5])
			with col3:
				st.write(f"P-Value : {res[1]:.10f}")
				st.write(f"Differencing : {d_val}")

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
		p_val = int(st.number_input(
        "Masukkan nilai untuk parameter P:",
        min_value=0,
        step=1,
        key="p_input"
    ))
  
		d_val = int(st.number_input(
        "Masukkan nilai untuk parameter D:",
        min_value=0,
        step=1,
        key="d_input"
    ))
  
		q_val = int(st.number_input(
        "Masukkan nilai untuk parameter Q:",
        min_value=0,
        step=1,
        key="q_input"
    ))

		calculate = st.button("Hitung")
	with col8:
		if calculate:
			model = ARIMA(data["value"], order=(p_val, d_val, q_val))
			fit_model = model.fit()

			st.write(fit_model.summary())

			forecast = fit_model.forecast(steps=12)

			st.subheader("Plot Forecast")
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

			mape_val = calculate_mape(df_plot["Actual"], df_plot["Predict"])
			st.write(f"Nilai MAPE: {mape_val}")