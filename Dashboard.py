import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from matplotlib.ticker import FuncFormatter

def workday_vs_holiday(df):
    hasil = df.groupby(by="workingday").agg({
    "casual": "sum",
    "registered": "sum",
    "cnt": "sum"
    })
    return hasil

def musim(df):
   hasil = df.groupby(by="season").cnt.sum() 
   return hasil

def cuaca(df):
    hasil = df.groupby(by="weathersit").cnt.sum()
    return hasil

def bulan(df):
    hasil = df.groupby(by="mnth").cnt.sum()
    return hasil

def jam(df):
    hasil = df.groupby(by="hr").cnt.sum()
    return hasil

def cluster(df):
    hasil = df.groupby(by="cluster").cnt.sum().reset_index()
    hasil.columns = ["Cluster", "Jumlah Peminjaman"]
    return hasil

day_df = pd.read_csv("day_df_final.csv")
hour_df = pd.read_csv("hour_df_final.csv")

day_df["dteday"] = pd.to_datetime(day_df["dteday"])
hour_df["dteday"] = pd.to_datetime(hour_df["dteday"])

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:
    st.image("https://cdn.pixabay.com/photo/2022/07/24/19/42/bike-7342379_1280.png")
    
    start_date, end_date = st.date_input(
        label="Interval Tanggal",min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

main_day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

main_hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

workday_vs_holiday_df = workday_vs_holiday(main_day_df)
musim_df = musim(main_day_df)
cuaca_df = cuaca(main_day_df)
bulan_df = bulan(main_day_df)
jam_df = jam(main_hour_df)
cluster_df = cluster(main_day_df)

st.header("Dashboard Peminjaman Sepeda :bike:")

st.subheader("Peminjaman sepeda di hari kerja vs hari libur")
fig, ax = plt.subplots()
workday_vs_holiday_df.plot(kind="bar", ax=ax)
ax.set_xlabel("0 = hari libur, 1 = hari kerja")
ax.set_ylabel("Jumlah peminjaman")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
st.pyplot(fig)

st.subheader("Peminjaman sepeda pada setiap musim")
fig, ax = plt.subplots()
musim_df.plot(kind="bar", ax=ax)
ax.set_xlabel("1 = Spring, 2 = Summer, 3 = Fall, 4 = Winter")
ax.set_ylabel("Jumlah")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
st.pyplot(fig)

st.subheader("Peminjaman sepeda pada setiap cuaca")
fig, ax = plt.subplots()
cuaca_df.plot(kind="bar", ax=ax)
ax.set_xlabel("1 = cerah, 2 = mendung/berawan, 3 = hujan/salju ringan")
ax.set_ylabel("Jumlah")
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, _: f"{int(x)}"))
st.pyplot(fig)

st.subheader("Peminjaman sepeda pada setiap bulannya")
hasil = bulan_df
fig, ax = plt.subplots()
ax.plot(hasil.index, hasil.values, marker="o", linestyle="-")
ax.set_xticks(range(1, 13))
ax.set_xticklabels(range(1, 13))
ax.set_xlabel("Bulan")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

st.subheader("Peminjaman sepeda pada setiap jamnya")
hasil = jam_df
fig, ax = plt.subplots()
ax.plot(hasil.index, hasil.values, marker="o", linestyle="-")
ax.set_xticks(range(0, 24))
ax.set_xticklabels(range(0, 24))
ax.set_xlabel("Jam")
ax.set_ylabel("Jumlah")
st.pyplot(fig)

st.subheader("Peminjaman sepeda berdasarkan suhu, kelembapan, dan kecepatan angin")
hasil = cluster_df
fig, ax = plt.subplots()
ax.bar(hasil["Cluster"], hasil["Jumlah Peminjaman"])
ax.set_xticks(hasil["Cluster"])
ax.set_xticklabels(hasil["Cluster"], rotation=90)
ax.set_xlabel("Cluster")
ax.set_ylabel("Jumlah")
st.pyplot(fig)