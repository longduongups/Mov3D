import streamlit as st
import sqlite3
import matplotlib.pyplot as plt

# Config
DB_NAME = "Data_IMU.db"

# Connexion à la base
def get_tables():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'TER_%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()
    return tables

# Lecture des données
def read_pitch_data(table_name):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(f"SELECT time, pitch, imu_name FROM {table_name} ORDER BY time ASC")
    rows = cursor.fetchall()
    conn.close()

    data = {"Haut": {"time": [], "pitch": []}, "Bas": {"time": [], "pitch": []}}
    for time, pitch, name in rows:
        if name in data:
            data[name]["time"].append(time)
            data[name]["pitch"].append(pitch)
    return data

# 📊 Affichage graphique
def plot_pitch(data, selected_table):
    fig, ax = plt.subplots(figsize=(10, 5))
    for name in data:
        ax.plot(data[name]["time"], data[name]["pitch"], label=f"Pitch {name}")
    ax.set_title(f"Historique Pitch - {selected_table}")
    ax.set_xlabel("Temps (ms)")
    ax.set_ylabel("Pitch (°)")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

# 🎯 Interface Streamlit
st.title("📈 Visualisation des sessions IMU")

tables = get_tables()
if not tables:
    st.warning("Aucune session enregistrée dans la base.")
else:
    selected_table = st.selectbox("Sélectionnez une session :", tables)
    data = read_pitch_data(selected_table)
    if st.button("Afficher le graphique"):
        plot_pitch(data, selected_table)
