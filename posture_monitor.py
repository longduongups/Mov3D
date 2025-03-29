# posture_monitor.py
import asyncio, struct, sqlite3
from datetime import datetime
from bleak import BleakClient

SENSOR_CHARACTERISTIC_UUID = "19B10001-E8F2-537E-4F6C-D104768A1214"
DEVICE_MAC = {"Haut": "F0:CF:41:E5:1F:D5", "Bas": "4C:EB:D6:4D:3B:BA"}
ANGLE_THRESHOLD = 20
calibrated_pitch = {}
latest_pitch = {}
stop_requested = False

async def read_characteristics(address, name, db_name, table_name):
    global stop_requested
    client = BleakClient(address)
    try:
        await client.connect()
        conn = sqlite3.connect(db_name)
        await asyncio.sleep(1)
        while not stop_requested:
            data = await client.read_gatt_char(SENSOR_CHARACTERISTIC_UUID)
            _, _, timer, orientation_data, _ = decode_sensor_data(data)
            pitch = orientation_data[1]
            latest_pitch[name] = pitch
            await asyncio.sleep(0.05)
    finally:
        await client.disconnect()

def decode_sensor_data(data):
    acc = struct.unpack('<fff', data[:12])
    gyro = struct.unpack('<fff', data[12:24])
    timer = struct.unpack('<I', data[24:28])[0]
    orientation = struct.unpack('<fff', data[28:40])
    steps = struct.unpack('<I', data[40:44])[0]
    return acc, gyro, timer, orientation, steps

async def run_monitor(db_name, table_name):
    tasks = [
        read_characteristics(address, name, db_name, table_name)
        for name, address in DEVICE_MAC.items()
    ]
    await asyncio.gather(*tasks)

def start_monitoring():
    global stop_requested
    stop_requested = False
    asyncio.run(run_monitor("Data_IMU.db", "PostureTable"))

def stop_monitoring():
    global stop_requested
    stop_requested = True

def calibrate():
    calibrated_pitch.update(latest_pitch)

def check_posture():
    for k in calibrated_pitch:
        if abs(latest_pitch.get(k, 0) - calibrated_pitch[k]) > ANGLE_THRESHOLD:
            return False
    return True
