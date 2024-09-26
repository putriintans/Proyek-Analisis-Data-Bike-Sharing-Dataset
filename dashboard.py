import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.set_page_config(layout="wide")

# Load dataset
day = pd.read_csv("day.csv")
hour = pd.read_csv("hour.csv")

# Merge datasets
bike_sharing = day.merge(hour, on='dteday', how='inner', suffixes=('_daily', '_hourly'))

# Membuat judul dashboard
st.title('Bike Rental Dashboard')

# Membuat summary untuk metrics
total_orders = day['cnt'].sum()
total_registered = day['registered'].sum()
total_casual = day['casual'].sum()

# Membuat kolom untuk metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Total Sharing Bike", value=total_orders)

with col2:
    st.metric("Total Registered", value=total_registered)

with col3:
    st.metric("Total Casual", value=total_casual)

# Grafik Penyewaan Sepeda Berdasarkan Kondisi Cuaca
st.subheader("Grafik Penyewaan Sepeda Berdasarkan Kondisi Cuaca")
colors = ["#E6D9A2", "#CB80AB", "#A594F9", "#0D7C66"]
fig, ax = plt.subplots(figsize=(10, 7))
sns.barplot(
    x="weathersit",  # Pastikan kolom ini ada dalam dataframe
    y="cnt",  # Menggunakan kolom 'cnt' dari dataframe yang benar
    data=hour.sort_values(by="weathersit", ascending=False),
    palette=colors,
    ax=ax
)
ax.set_title("Jumlah Penyewa Sepeda Berdasarkan Kondisi Cuaca", loc="center", fontsize=15)
ax.set_ylabel('Jumlah Penyewa')
ax.set_xlabel('Kondisi Cuaca')
ax.tick_params(axis='x', labelsize=12, rotation=25)
ax.tick_params(axis='y', labelsize=12)
st.pyplot(fig)

# Perbandingan Customer yang Registered dengan Casual
st.subheader("Perbandingan Customer yang Registered dengan Casual")
data = [total_casual, total_registered]
labels = ['Casual', 'Registered']

fig1, ax1 = plt.subplots()
ax1.pie(data, labels=labels, autopct='%2.2f%%', colors=["#EECAD5", "#D1E9F6"])
st.pyplot(fig1)

# Distribusi pengguna Registered pada saat Workingday vs Weekend
st.subheader("Distribusi pengguna Registered pada saat Workingday vs Weekend")

# Memfilter data untuk weekend (contoh: hari Sabtu dan Minggu)
weekend_data = day[day['workingday'] == 0]['registered'].dropna()
# Memfilter data untuk working days (contoh: hari kerja)
workingdays_data = day[day['workingday'] == 1]['registered'].dropna()

fig2, ax2 = plt.subplots(figsize=(14, 7))
sns.histplot(weekend_data, bins=30, label='Weekend Days', color='blue', kde=True, alpha=0.5, ax=ax2)
sns.histplot(workingdays_data, bins=30, label='Working Days', color='orange', kde=True, alpha=0.5, ax=ax2)

ax2.set_xlabel('Registered Rides')
ax2.set_ylabel('Frekuensi')
ax2.set_title('Grafik Penyewa Sepeda Working vs Weekend Days')
ax2.legend()
st.pyplot(fig2)
