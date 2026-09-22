import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

connection = psycopg2.connect(
    os.getenv("DATABASE_URL")
)

cursor = connection.cursor()

cursor.execute("""
ALTER TABLE categories
ADD COLUMN IF NOT EXISTS count_text VARCHAR(100);
""")

cursor.execute("""
UPDATE categories
SET count_text = CASE name
    WHEN 'Security' THEN '2 Cameras'
    WHEN 'Climate' THEN '2 AC'
    WHEN 'Climate-Con' THEN '2 AC'
    WHEN 'Sensors' THEN 'Humidity & Air'
    WHEN 'Appliances' THEN '1 Fridge'
    WHEN 'Lighting' THEN '5 Devices'
    WHEN 'Remote Lock' THEN '6 Doors'
    WHEN 'Entertainment' THEN '2 TV'
    WHEN 'Energy' THEN 'Usage Insights'
    ELSE 'No data'
END;
""")

connection.commit()

print("Category count data updated successfully.")

cursor.close()
connection.close()