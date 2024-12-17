import pandas as pd
import mysql.connector

# Koneksi ke database
conn = mysql.connector.connect(
    host="localhost",
    user="arifrizqy",
    password="@Arriz2401",
    database="forecasting_db"
)

# Baca file CSV
data = pd.read_csv('data-source/data.csv')

# Sisipkan data secara batch
cursor = conn.cursor()
query = "INSERT INTO forecast_data (date, value) VALUES (%s, %s)"
values = list(data.itertuples(index=False, name=None))
cursor.executemany(query, values)
conn.commit()

print(f"{cursor.rowcount} rows inserted.")
conn.close()
