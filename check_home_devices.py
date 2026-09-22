import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
SELECT id, name, device_type, room, status, power_watts
FROM devices
WHERE name IN (
    'Smart Webcam',
    'Stereo Speaker',
    'Room Light'
)
ORDER BY id;
""")

for device in cursor.fetchall():
    print(device)

cursor.close()
connection.close()