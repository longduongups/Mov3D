import sqlite3

# Connexion à la base
conn = sqlite3.connect("Data_IMU.db")
cursor = conn.cursor()

# Récupérer toutes les tables commençant par "TER_2024"
cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'TER_2024%'")
tables_2024 = [row[0] for row in cursor.fetchall()]

# Supprimer chaque table trouvée
for table in tables_2024:
    cursor.execute(f"DROP TABLE IF EXISTS {table}")
    print(f"🗑️ Supprimée : {table}")

conn.commit()
conn.close()
print(f"\n✅ {len(tables_2024)} table(s) supprimée(s) de 2024.")