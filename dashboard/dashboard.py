import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

# Judul untuk Dashboard
st.title('Dashboard Analisis Penjualan E-Commerce')

@st.cache
def load_data():
    orders_data = pd.read_csv('dashboard/E Commerce Public Dataset/orders_dataset.csv')
    order_items_data = pd.read_csv('dashboard/E Commerce Public Dataset/order_items_dataset.csv')
    products_data = pd.read_csv('dashboard/E Commerce Public Dataset/products_dataset.csv')
    order_reviews_data = pd.read_csv('dashboard/E Commerce Public Dataset/order_reviews_dataset.csv')
    return orders_data, order_items_data, products_data, order_reviews_data

# Load data
orders_data, order_items_data, products_data, order_reviews_data = load_data()

# Menggabungkan dataset
try:
    merged_data = pd.merge(orders_data, order_items_data, on='order_id', how='inner')
    merged_data = pd.merge(merged_data, products_data[['product_id', 'product_category_name']], on='product_id', how='inner')
    merged_data = pd.merge(merged_data, order_reviews_data[['order_id', 'review_score']], on='order_id', how='inner')
except Exception as e:
    st.error(f"Error merging data: {e}")
    st.stop()

# filter interaktif
st.sidebar.title("Filters")
date_filter = st.sidebar.date_input("Select Date Range", [], key='date_range_filter')
category_filter = st.sidebar.multiselect("Select Product Categories", merged_data['product_category_name'].unique(), key='category_filter')

# filter berdasarkan input pengguna
if date_filter:
    try:
        merged_data['order_purchase_timestamp'] = pd.to_datetime(merged_data['order_purchase_timestamp'])
        if len(date_filter) == 2:
            start_date, end_date = date_filter
            merged_data = merged_data[(merged_data['order_purchase_timestamp'] >= pd.to_datetime(start_date)) &
                                      (merged_data['order_purchase_timestamp'] <= pd.to_datetime(end_date))]
    except Exception as e:
        st.error(f"Error applying date filter: {e}")

if category_filter:
    try:
        merged_data = merged_data[merged_data['product_category_name'].isin(category_filter)]
    except Exception as e:
        st.error(f"Error applying category filter: {e}")

# Pastikan data yang di-filter tidak kosong
if merged_data.empty:
    st.write("Tidak ada data yang sesuai dengan filter yang diterapkan.")
else:
    # Pertanyaan 1: Berapa banyak jumlah top penjualan per kategori produk
    st.subheader('Top 10 Kategori Produk Berdasarkan Penjualan')

    try:
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
    except Exception as e:
        st.error(f"Error plotting top categories: {e}")

# Pertanyaan 2: Analisis Harga Produk dan Ulasan Pelanggan dalam 3 bulan terakhir
    st.subheader('Analisis Harga Produk dan Ulasan Pelanggan dalam 3 Bulan Terakhir')

    try:
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
    except Exception as e:
        st.error(f"Error analyzing price and review: {e}")
