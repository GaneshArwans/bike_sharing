import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import datetime
from pathlib import Path

def sidebar(df):
    df["dteday"] = pd.to_datetime(df["dteday"])
    min_date = df["dteday"].min()
    max_date = df["dteday"].max()

    with st.sidebar:
        st.image("https://freepngimg.com/thumb/bicycle/6-2-bicycle-png-7.png")

        def on_change():
            st.session_state.date = date

        date = st.date_input(
            label="Rentang Waktu",
            min_value=min_date,
            max_value=max_date,
            value=[min_date, max_date],
            on_change=on_change
        )
    return date

def season(df):
    st.subheader("Rata-rata Jumlah Peminjaman Per Musim")
    season_avg = df.groupby('season')['cnt'].mean().sort_index()
    season_labels = ['Fall', 'Spring', 'Summer', 'Winter']
    fig = plt.figure(figsize=(20, 10))
    plt.bar(season_labels, season_avg)
    plt.xlabel("Season", fontsize=18)
    plt.ylabel("Rata-rata Jumlah Peminjaman", fontsize=18)
    plt.title("Rata-rata Jumlah Peminjaman Per Musim", fontsize=20)
    st.pyplot(fig)

def workingday(df):
    st.subheader("Rata-rata Jumlah Peminjaman Sepeda Per Jam")
    hourly_rentals = df.groupby(["hr", "workingday"])["cnt"].mean().reset_index()
    fig = plt.figure(figsize=(10, 6))
    sns.barplot(data=hourly_rentals, x="hr", y="cnt", hue="workingday")
    plt.title("Rata-rata Jumlah Peminjaman Sepeda per Jam",fontsize=18)
    plt.xlabel("Jam dalam Sehari",fontsize=18)
    plt.ylabel("Rata-rata Jumlah Peminjaman Sepeda",fontsize=15)
    plt.xticks(rotation=0)
    plt.legend(title="Working day")
    plt.grid(axis="y")
    st.pyplot(fig)

if __name__ == "__main__":
    sns.set(style="dark")
    st.header("Bike Sharing Streamlit Dashboard")

    day_df = pd.read_csv(Path(__file__).parents[1] / 'dashboard/day_clean.csv')
    hour_df = pd.read_csv(Path(__file__).parents[1] / 'dashboard/hour_clean.csv')

    date = sidebar(day_df)
    if(len(date) == 2):
        main_df = day_df[(day_df["dteday"] >= str(date[0])) & (day_df["dteday"] <= str(date[1]))]
    else:
        main_df = day_df[(day_df["dteday"] >= str(st.session_state.date[0])) & (day_df["dteday"] <= str(st.session_state.date[1]))]

    season(main_df)
    workingday(hour_df)

    year_c = datetime.date.today().year
    copyright = "Copyright © " + str(year_c) + " William "
    st.caption(copyright)

