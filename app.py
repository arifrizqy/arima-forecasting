import mysql.connector
import pandas as pd
import streamlit as st

from statsmodels.tsa.arima.model import ARIMA

def get_connection():
    return mysql.connector.connect(
        host="localhost",
        user="arifrizqy",
        password="@Arriz2401",
        database="forecasting_db"
      )

def fetch_data():
    conn = get_connection()
    query = "SELECT * FROM forecast_data ORDER BY date"
    df = pd.read_sql(query, conn)
    conn.close()
    return df

def add_data(date, value):
    conn = get_connection()
    cursor = conn.cursor()
    query = "INSERT INTO forecast_data (date, value) VALUES (%s, %s)"
    cursor.execute(query, (date, value))
    conn.commit()
    conn.close()

def delete_data(row_id):
    conn = get_connection()
    cursor = conn.cursor()
    query = "DELETE FROM forecast_data WHERE id = %s"
    cursor.execute(query, (row_id,))
    conn.commit()
    conn.close()

def get_time_series():
    df = fetch_data()
    df['date'] = pd.to_datetime(df['date'])
    df.set_index('date', inplace=True)
    return df['value']

def train_arima(ts, order=(1, 1, 1)):
    model = ARIMA(ts, order=order)
    model_fit = model.fit()
    return model_fit

def forecast(model, steps=12):
    forecast = model.forecast(steps=steps)
    return forecast
  
def predict(model, end=0, start=0):
    predict = model.predict(start=start, end=end)
    return predict

st.title("Aplikasi Peramalan dengan ARIMA")
st.header("Data")
df = fetch_data()
st.write(df)

st.subheader("Tambah Data")
date = st.date_input("Tanggal")
value = st.number_input("Nilai", step=1.0)
if st.button("Tambah"):
    add_data(date, value)
    st.success("Data berhasil ditambahkan!")

st.subheader("Hapus Data")
id_to_delete = st.number_input("ID Data untuk dihapus", step=1)
if st.button("Hapus"):
    delete_data(id_to_delete)
    st.success("Data berhasil dihapus!")

st.subheader("Data Actual")
ts = get_time_series()
st.line_chart(ts)

st.subheader("Hasil Predict")
ts = get_time_series()
model = train_arima(ts)
predict_values = predict(model, len(ts)-1)
st.line_chart(predict_values)

st.subheader("Hasil Peramalan")
ts = get_time_series()
model = train_arima(ts)
forecast_values = forecast(model)
st.line_chart(forecast_values)

combined_df = pd.DataFrame({
                "Series": df['date'],
                "Aktual": df['value'],
                "Forecast": predict_values
              })

st.plotly_chart(combined_df)
