# Nama file: dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Membaca dataset
df = pd.read_csv('all_datanew.csv')

# Menampilkan judul
st.title('Dashboard Sederhana coy')

# Menampilkan data
st.write('Data E-commerce publik:')
st.write(df.head())

# Statistik deskriptif
st.write('Statistik Deskriptif:')
st.write(df.describe())

# Menampilkan grafik
st.write('Grafik Histogram:')
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

# Pilih kolom untuk histogram
column = st.selectbox('Pilih kolom untuk histogram:', numeric_columns)

fig, ax = plt.subplots()
ax.hist(df[column].dropna(), bins=20, edgecolor='black')
ax.set_title(f'Histogram dari {column}')
ax.set_xlabel(column)
ax.set_ylabel('Frekuensi')
st.pyplot(fig)
