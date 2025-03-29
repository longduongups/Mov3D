import threading
import asyncio
from bleak import BleakClient
import struct
import sqlite3
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt

# UUIDs des caractéristiques
SENSOR_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
DEVICE_MAC = {
    "Haut": "F0:CF:41:E5:1F:D5",
    "Bas": "4C:EB:D6:4D:3B:BA",
}

# Variables globales
stop_requested = False
monitor_angle = False
latest_pitch = {"Haut": None, "Bas": None}
calibrated_pitch = {"Haut": None, "Bas": None}
ANGLE_THRESHOLD = 20

# Base de données
date_hour_DBTable = datetime.now().strftime("TER_%Y%m%d_%H%M")
db_name = "Data_IMU.db"

def decode_sensor_data(data):
    if len(data) != 50:
        raise ValueError("La taille des données n'est pas correcte")
    acc_data = struct.unpack('<fff', data[:12])
    gyro_data = struct.unpack('<fff', data[12:24])
    timer = struct.unpack('<I', data[24:28])[0]
    orientation_data = struct.unpack('<fff', data[28:40])
    steps_data = struct.unpack('<I', data[40:44])[0]
    return acc_data, gyro_data, timer, orientation_data, steps_data

def connect_to_database(db_name):
    return sqlite3.connect(db_name)

def create_table(conn):
    cursor = conn.cursor()
    str_execute = f'''
    CREATE TABLE IF NOT EXISTS {date_hour_DBTable} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        time REAL NOT NULL,
        imu_name TEXT NOT NULL,
        acc_x REAL, acc_y REAL, acc_z REAL,
        gyro_x REAL, gyro_y REAL, gyro_z REAL,
        heading REAL, pitch REAL, roll REAL,
        steps INTEGER, processed INTEGER,
        velocity_x REAL, velocity_y REAL, velocity_z REAL,
        position_x REAL, position_y REAL, position_z REAL
    )'''
    cursor.execute(str_execute)
    conn.commit()

def insert_sensor_data(conn, time, imu_name, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, heading, pitch, roll, steps):
    cursor = conn.cursor()
    cursor.execute(f'''
        INSERT INTO {date_hour_DBTable}(
            time, imu_name, acc_x, acc_y, acc_z,
            gyro_x, gyro_y, gyro_z,
            heading, pitch, roll, steps, processed
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
        (time, imu_name, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, heading, pitch, roll, steps, 0))
    conn.commit()

async def read_characteristics(address, name):
    global stop_requested
    client = BleakClient(address)
    try:
        await client.connect()
        print(f"Connecté à {name}")
        conn = connect_to_database(db_name)
        create_table(conn)
        timer_offset = 0
        first_value = False

        while client.is_connected and not stop_requested:
            data_sensor = await client.read_gatt_char(SENSOR_CHARACTERISTIC_UUID)
            acc_data, gyro_data, timer, orientation_data, steps_data = decode_sensor_data(data_sensor)
            if not first_value:
                timer_offset = timer
                first_value = True

            time_val = timer - timer_offset
            insert_sensor_data(conn, time_val, name, *acc_data, *gyro_data, *orientation_data, steps_data)
            latest_pitch[name] = orientation_data[1]

            print(f"{name} - Pitch: {orientation_data[1]:.2f}")
            await asyncio.sleep(0.05)

    except Exception as e:
        print(f"Erreur avec {name}: {e}")
    finally:
        await client.disconnect()

async def main():
    tasks = [read_characteristics(address, name) for name, address in DEVICE_MAC.items()]
    await asyncio.gather(*tasks)

def run():
    asyncio.run(main())

def start_measurement():
    global stop_requested
    stop_requested = False
    threading.Thread(target=run).start()

def calibrate_orientation():
    if latest_pitch["Haut"] is not None and latest_pitch["Bas"] is not None:
        calibrated_pitch["Haut"] = latest_pitch["Haut"]
        calibrated_pitch["Bas"] = latest_pitch["Bas"]
        status_label.config(text="✅ Calibration faite. Bonne posture enregistrée.")
        global monitor_angle
        monitor_angle = True
    else:
        messagebox.showwarning("Calibration", "Pitch non disponible. Assurez-vous que les capteurs envoient des données.")

def stop_measurement():
    global stop_requested, monitor_angle
    stop_requested = True
    monitor_angle = False
    status_label.config(text="⏹️ Mesure arrêtée.")

def update_ui():
    if monitor_angle:
        haut = latest_pitch.get("Haut")
        bas = latest_pitch.get("Bas")
        pitch_calib_haut = calibrated_pitch.get("Haut")
        pitch_calib_bas = calibrated_pitch.get("Bas")

        if None not in (haut, bas, pitch_calib_haut, pitch_calib_bas):
            ecart_haut = abs(haut - pitch_calib_haut)
            ecart_bas = abs(bas - pitch_calib_bas)

            if ecart_haut > ANGLE_THRESHOLD or ecart_bas > ANGLE_THRESHOLD:
                status_label.config(
                    text=f"❌ Mauvaise posture\nΔ Haut: {ecart_haut:.1f}°, Δ Bas: {ecart_bas:.1f}°"
                )
            else:
                status_label.config(
                    text=f"✅ Bonne posture\nΔ Haut: {ecart_haut:.1f}°, Δ Bas: {ecart_bas:.1f}°"
                )
    root.after(500, update_ui)

# 📈 Fonction d'affichage de l’historique du pitch
def show_pitch_history():
    # Connexion à la base
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Récupère toutes les tables TER_...
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'TER_%'")
    tables = [row[0] for row in cursor.fetchall()]
    conn.close()

    if not tables:
        messagebox.showinfo("Info", "Aucune session enregistrée.")
        return

    # Fenêtre de sélection
    def plot_selected_table():
        selected_table = table_var.get()
        plot_pitch_from_table(selected_table)
        selector.destroy()

    selector = tk.Toplevel(root)
    selector.title("Choisir une session à afficher")

    tk.Label(selector, text="📁 Sélectionnez une session :").pack(pady=5)
    table_var = tk.StringVar(selector)
    table_var.set(tables[0])
    tk.OptionMenu(selector, table_var, *tables).pack(pady=5)
    tk.Button(selector, text="Afficher le graphique", command=plot_selected_table).pack(pady=10)
def plot_pitch_from_table(table_name):
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        cursor.execute(f'''
            SELECT time, pitch, imu_name FROM {table_name}
            ORDER BY time ASC
        ''')
        rows = cursor.fetchall()
        conn.close()
    except Exception as e:
        messagebox.showerror("Erreur", f"Lecture impossible : {e}")
        return

    time_haut, pitch_haut = [], []
    time_bas, pitch_bas = [], []

    for time, pitch, name in rows:
        if name == "Haut":
            time_haut.append(time)
            pitch_haut.append(pitch)
        elif name == "Bas":
            time_bas.append(time)
            pitch_bas.append(pitch)

    if not time_haut and not time_bas:
        messagebox.showinfo("Info", "Pas de données exploitables.")
        return

    plt.figure(figsize=(12, 6))
    if time_haut:
        plt.plot(time_haut, pitch_haut, label="Capteur Haut", linewidth=1.5)
    if time_bas:
        plt.plot(time_bas, pitch_bas, label="Capteur Bas", linewidth=1.5)

    plt.title(f"Pitch dans le temps - {table_name}")
    plt.xlabel("Temps (ms)")
    plt.ylabel("Pitch (°)")
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Interface utilisateur
root = tk.Tk()
root.title("Interface IMU - Contrôle de posture")

tk.Button(root, text="▶️ Start", width=25, command=start_measurement).pack(pady=5)
tk.Button(root, text="🎯 Calibrer (Bonne posture)", width=25, command=calibrate_orientation).pack(pady=5)
tk.Button(root, text="⏹️ Stop", width=25, command=stop_measurement).pack(pady=5)
tk.Button(root, text="📈 Afficher l'historique", width=25, command=show_pitch_history).pack(pady=5)

status_label = tk.Label(root, text="🕐 En attente de démarrage...", font=("Arial", 12))
status_label.pack(pady=15)

update_ui()
root.mainloop()
