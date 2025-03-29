from bleak import BleakScanner

async def scan_ble_devices():
    devices = await BleakScanner.discover()
    print("Liste des périphériques Bluetooth Low Energy (BLE) trouvés :")
    for device in devices:
        print(f"Nom: {device.name}, Adresse MAC: {device.address}")

if __name__ == "__main__":
    import asyncio
    asyncio.run(scan_ble_devices())