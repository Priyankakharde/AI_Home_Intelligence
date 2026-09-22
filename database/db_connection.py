import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text

# Load variables from .env
load_dotenv()

# Get database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# Create database engine
engine = create_engine(DATABASE_URL)

# Test connection
with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("PostgreSQL connection successful!")
    print("Test result:", result.scalar())