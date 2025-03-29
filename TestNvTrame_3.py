import threading
import asyncio
from bleak import BleakClient
import struct
import sqlite3
from datetime import datetime
import os

# UUIDs des caractéristiques pour tous les appareils
SENSOR_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"

# Mapping des noms d'appareils aux adresses MAC
DEVICE_MAC = {
    #"Cuisse_Gauche": "C7:8F:CB:8B:57:E1",
    "Cuisse_Droite": "F0:CF:41:E5:1F:D5",
    "Tibia_Droit": "4C:EB:D6:4D:3B:BA",
    #"Tibia_Gauche": "A9:58:51:94:8C:C9"
}

# Variable pour indiquer si l'utilisateur a demandé l'arrêt de la connexion
stop_requested = False

# Obtention de la date et de l'heure actuelles pour nommer la table de la base de données
date_hour_DBTable =datetime.now().strftime("TER_%Y%m%d_%H%M")

#Nom de la base de donnée
db_name="Data_IMU.db"

def decode_sensor_data(data):
    # Vérifier que la longueur des données est correcte
    if len(data) != 50:
        raise ValueError("La taille des données n'est pas correcte")
    
    # Décompresser les données en récupérant les valeurs d'accéléromètre, de gyroscope et du timer
    acc_data = struct.unpack('<fff', data[:12])  # Les données d'accéléromètre sont les 12 premiers octets
    gyro_data = struct.unpack('<fff', data[12:24])  # Les données de gyroscope sont les octets de 12 à 24
    timer = struct.unpack('<I', data[24:28])[0]  # Le timer est sur 4 octets de 24 à 28
    orientation_data = struct.unpack('<fff', data[28:40])  # Les données d'orientation sont les octets restants
    steps_data = struct.unpack('<I', data[40:44])[0]  # Le timer est sur 4 octets de 40 à 44

    return acc_data, gyro_data, timer, orientation_data, steps_data

# Fonction pour se connecter à la base de données
def connect_to_database(db_name):
    conn = sqlite3.connect(db_name)
    return conn

# Fonction pour créer la table si elle n'existe pas
def create_table(conn):
    cursor = conn.cursor()
    str_execute = '''CREATE TABLE IF NOT EXISTS '''+ date_hour_DBTable + '''(
                        ID INTEGER PRIMARY KEY AUTOINCREMENT,
                        time REAL NOT NULL,
                        imu_name TEXT NOT NULL,
                        acc_x REAL,
                        acc_y REAL,
                        acc_z REAL,
                        gyro_x REAL,
                        gyro_y REAL,
                        gyro_z REAL,
                        heading REAL,
                        pitch REAL,
                        roll REAL,
                        steps INTEGER,
                        processed INTEGER,
                        velocity_x REAL,
                        velocity_y REAL,
                        velocity_z REAL,
                        position_x REAL,
                        position_y REAL,
                        position_z REAL
                    )'''
    cursor.execute(str_execute)
    conn.commit()

# Fonction pour insérer les données des capteurs dans la table
def insert_sensor_data(conn, time, imu_name, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, heading, pitch, roll, steps):
    cursor = conn.cursor()
    cursor.execute('''INSERT INTO ''' + date_hour_DBTable + '''(time, imu_name, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, heading, pitch, roll, steps, processed)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (time, imu_name, acc_x, acc_y, acc_z, gyro_x, gyro_y, gyro_z, heading, pitch, roll, steps,0))
    conn.commit()


async def read_characteristics(address, name):
    global stop_requested
    client = BleakClient(address)
    try:
        await client.connect()
        
        print(f"Lecture des caractéristiques de {name}:")

        # Initialisation de l'offset du Timer pour que la première valeur récupérée soit la référence
        timer_offset = 0

        # Initialisation de la variable pour savoir si on est sur la première mesure de la série ("False" au début et "True" une fois dans la série) pour l'initialisation de l'offset 
        first_value=False
        
        # Connexion à la base de données SQLite
        conn = connect_to_database(db_name)
        create_table(conn)
        while client.is_connected and not stop_requested:
            # Lecture de la caractéristique d'accélération
            data_sensor = await client.read_gatt_char(SENSOR_CHARACTERISTIC_UUID)
            acc_data, gyro_data, timer, orientation_data, steps_data = decode_sensor_data(data_sensor)

            #initialisation de l'offset du timer
            if first_value==False:
                timer_offset = timer
                first_value = True
            
            # Insertion des données dans la base de données
            insert_sensor_data(conn, timer-timer_offset, name, *acc_data, *gyro_data, *orientation_data, steps_data)
            if timer-timer_offset > 10000:
                stop_requested = True
            # Affichage des données lues
            print(f"{name} - Acceleration Data:", acc_data)
            print(f"{name} - Gyroscope Data:", gyro_data)
            print(f"{name} - Timer Data:", timer-timer_offset)
            print(f"{name} - Orientation:", orientation_data)
            print(f"{name} - Steps_data:", steps_data)

    
    except Exception as e:
        print(e)
    finally:
        await client.disconnect()
        #conn.close()  # Fermeture de la connexion à la base de données
        os._exit(0)

async def main():
    tasks = []
    for name, address in DEVICE_MAC.items():
        tasks.append(read_characteristics(address, name))
    await asyncio.gather(*tasks)

# Fonction pour lancer le programme en utilisant asyncio
def run():
    asyncio.run(main())

# Fonction pour arrêter le programme sur commande
def stop():
    global stop_requested
    input("Appuyez sur Entrée pour arrêter la connexion...")
    stop_requested = True

# Lancement des threads pour exécuter les tâches de lecture en parallèle
threads = []
stop_thread = threading.Thread(target=stop)
stop_thread.start()

for _ in range(len(DEVICE_MAC)):
    thread = threading.Thread(target=run)
    thread.start()
    threads.append(thread)

# Attente de la fin de tous les threads
for thread in threads:
    thread.join()
    

