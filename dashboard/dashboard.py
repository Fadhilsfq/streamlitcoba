import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Judul untuk Dashboard
st.title('Dashboard Analisis Penjualan E-Commerce')

@st.cache
def load_data():
    orders_data = pd.read_csv('D:\\UNNES\\Kegabutan\\Dicoding\\Latihan Data\\Submission Muhammad Syafiq Fadhilah terbaru\\E-Commerce Public Dataset\\orders_dataset.csv')
    order_items_data = pd.read_csv('D:\\UNNES\\Kegabutan\\Dicoding\\Latihan Data\\Submission Muhammad Syafiq Fadhilah terbaru\\E-Commerce Public Dataset\\order_items_dataset.csv')
    products_data = pd.read_csv('D:\\UNNES\\Kegabutan\\Dicoding\\Latihan Data\\Submission Muhammad Syafiq Fadhilah terbaru\\E-Commerce Public Dataset\\products_dataset.csv')
    order_reviews_data = pd.read_csv('D:\\UNNES\\Kegabutan\\Dicoding\\Latihan Data\\Submission Muhammad Syafiq Fadhilah terbaru\\E-Commerce Public Dataset\\order_reviews_dataset.csv')
    return orders_data, order_items_data, products_data, order_reviews_data

# Load data
orders_data, order_items_data, products_data, order_reviews_data = load_data()

# Menggabungkan dataset
merged_data = pd.merge(orders_data, order_items_data, on='order_id', how='inner')
merged_data = pd.merge(merged_data, products_data[['product_id', 'product_category_name']], on='product_id', how='inner')
merged_data = pd.merge(merged_data, order_reviews_data[['order_id', 'review_score']], on='order_id', how='inner')

# Pertanyaan 1: Berapa banyak jumlah top penjualan per kategori produk
st.subheader('Top 10 Kategori Produk Berdasarkan Penjualan')

# Group by product category and count orders
category_sales_total = merged_data['product_category_name'].value_counts()

# Plot top categories
plt.figure(figsize=(12, 8))
category_sales_total.head(10).plot(kind='barh', color='skyblue')
plt.title('Top 10 Kategori Produk Berdasarkan Penjualan')
plt.xlabel('Jumlah Penjualan')
plt.ylabel('Kategori Produk')
plt.grid(axis='x', linestyle='--', alpha=0.7)
st.pyplot(plt)

# Pertanyaan 2: Analisis Harga Produk dan Ulasan Pelanggan dalam 3 bulan terakhir
st.subheader('Analisis Harga Produk dan Ulasan Pelanggan dalam 3 Bulan Terakhir')

# Sekarang menggunakan 'merged_data' untuk analisis harga dan ulasan
data_clean_price_review = merged_data.dropna(subset=['price', 'review_score'])

# Scatter plot untuk menunjukkan korelasi
plt.figure(figsize=(12, 8))
sns.scatterplot(x='price', y='review_score', data=data_clean_price_review)
plt.title('Korelasi antara Harga Produk dan Skor Ulasan')
plt.xlabel('Harga Produk')
plt.ylabel('Skor Ulasan')
plt.grid(True)
st.pyplot(plt)

# Menghitung koefisien korelasi
correlation = data_clean_price_review[['price', 'review_score']].corr()
st.write(f"Koefisien korelasi: {correlation.loc['price', 'review_score']}")
