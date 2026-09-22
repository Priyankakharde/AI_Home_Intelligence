import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
INSERT INTO devices
    (name, device_type, room, status, power_watts)
VALUES
    ('Smart Webcam', 'Camera', 'Living Room', TRUE, 15),
    ('Stereo Speaker', 'Speaker', 'Living Room', TRUE, 8),
    ('Room Light', 'Light', 'Living Room', FALSE, 12)
ON CONFLICT DO NOTHING;
""")

connection.commit()

print("Home devices added successfully.")

cursor.close()
connection.close()