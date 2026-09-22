# ============================================================
# AI HOME INTELLIGENCE
# FastAPI Backend
# ============================================================

from pathlib import Path
import os
import joblib
from dotenv import load_dotenv

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


# ============================================================
# APP CONFIG
# ============================================================

app = FastAPI(
    title="AI Home Intelligence API",
    description="Backend API for Smart Home Monitoring and Machine Learning",
    version="1.0.0",
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# PROJECT PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent

MODEL_DIR = BASE_DIR / "models"

ENERGY_MODEL_PATH = MODEL_DIR / "energy_model.pkl"
ANOMALY_MODEL_PATH = MODEL_DIR / "anomaly_model.pkl"


# ============================================================
# DATABASE CONFIG
# ============================================================

load_dotenv(BASE_DIR / ".env")
DATABASE_URL = os.getenv("DATABASE_URL")


def get_database_connection():
    """
    Create a PostgreSQL database connection.

    The DATABASE_URL is loaded from the environment.
    """

    if not DATABASE_URL:
        raise RuntimeError(
            "DATABASE_URL is not set. "
            "Please check your .env file."
        )

    return psycopg2.connect(
        DATABASE_URL
    )


# ============================================================
# LOAD ML MODELS
# ============================================================

energy_model = None
anomaly_model = None


def load_models():
    """
    Load trained ML models from the models folder.
    """

    global energy_model
    global anomaly_model

    # Energy prediction model
    if ENERGY_MODEL_PATH.exists():

        with open(
            ENERGY_MODEL_PATH,
            "rb"
        ) as file:

            energy_model = joblib.load(file)

    # Anomaly detection model
    if ANOMALY_MODEL_PATH.exists():

        with open(
            ANOMALY_MODEL_PATH,
            "rb"
        ) as file:

            anomaly_model = joblib.load(file)


load_models()


# ============================================================
# ROOT ENDPOINT
# ============================================================

@app.get("/")
def root():

    return {
        "message": "AI Home Intelligence API is running",
        "status": "online",
        "database": "PostgreSQL",
        "machine_learning": {
            "energy_prediction": energy_model is not None,
            "anomaly_detection": anomaly_model is not None,
        },
    }


# ============================================================
# HEALTH CHECK
# ============================================================

@app.get("/health")
def health_check():

    database_status = "disconnected"

    try:

        connection = get_database_connection()

        connection.close()

        database_status = "connected"

    except Exception:

        database_status = "disconnected"

    return {
        "status": "healthy",
        "database": database_status,
        "energy_model": energy_model is not None,
        "anomaly_model": anomaly_model is not None,
    }


# ============================================================
# GET DEVICES
# ============================================================

@app.get("/devices")
def get_devices():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id,
                name,
                device_type,
                room,
                status,
                power_watts
            FROM devices
            ORDER BY id;
            """
        )

        devices = cursor.fetchall()

        return [
            dict(device)
            for device in devices
        ]

    finally:

        cursor.close()
        connection.close()
        
# ============================================================
# CATEGORIES
# ============================================================

@app.get("/categories")
def get_categories():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute("""
            SELECT
                id,
                name,
                icon,
                description,
                status,
                created_at
            FROM categories
            ORDER BY id;
        """)

        categories = cursor.fetchall()

        return {
            "success": True,
            "categories": [
                dict(category)
                for category in categories
            ]
        }

    finally:

        cursor.close()
        connection.close()        


@app.post("/categories")
def add_category(
    name: str,
    icon: str = "",
    description: str = "",
    status: bool = True
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            INSERT INTO categories
                (name, icon, description, status)
            VALUES
                (%s, %s, %s, %s)
            RETURNING
                id,
                name,
                icon,
                description,
                status,
                created_at;
            """,
            (
                name,
                icon,
                description,
                status
            )
        )

        category = cursor.fetchone()

        connection.commit()

        return {
            "success": True,
            "category": dict(category)
        }

    finally:

        cursor.close()
        connection.close()


@app.put("/categories/{category_id}")
def update_category(
    category_id: int,
    name: str,
    icon: str = "",
    description: str = "",
    status: bool = True
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            UPDATE categories
            SET
                name = %s,
                icon = %s,
                description = %s,
                status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                icon,
                description,
                status,
                created_at;
            """,
            (
                name,
                icon,
                description,
                status,
                category_id
            )
        )

        category = cursor.fetchone()

        if category is None:

            connection.rollback()

            return {
                "success": False,
                "message": "Category not found"
            }

        connection.commit()

        return {
            "success": True,
            "category": dict(category)
        }

    finally:

        cursor.close()
        connection.close()


@app.delete("/categories/{category_id}")
def delete_category(category_id: int):

    connection = get_database_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM categories
            WHERE id = %s;
            """,
            (category_id,)
        )

        if cursor.rowcount == 0:

            connection.rollback()

            return {
                "success": False,
                "message": "Category not found"
            }

        connection.commit()

        return {
            "success": True,
            "message": "Category deleted successfully"
        }

    finally:

        cursor.close()
        connection.close()        
        

# ============================================================
# UPDATE DEVICE STATUS
# ============================================================

@app.put("/devices/{device_id}/status")
def update_device_status(
    device_id: int,
    status: bool
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            UPDATE devices
            SET status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                device_type,
                room,
                status,
                power_watts;
            """,
            (
                status,
                device_id
            )
        )

        device = cursor.fetchone()

        if device is None:

            connection.rollback()

            return {
                "success": False,
                "message": "Device not found"
            }

        connection.commit()

        return {
            "success": True,
            "device": dict(device)
        }

    finally:

        cursor.close()
        connection.close()        
        
# ============================================================
# GET USERS
# ============================================================

@app.get("/users")
def get_users():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id,
                name,
                role,
                avatar,
                status,
                created_at
            FROM users
            ORDER BY id;
            """
        )

        users = cursor.fetchall()

        return [
            dict(user)
            for user in users
        ]

    finally:

        cursor.close()
        connection.close()       
        
# ============================================================
# ADD USER
# ============================================================

@app.post("/users")
def add_user(
    name: str,
    role: str = "Member",
    avatar: str = "👤",
    status: bool = True
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            INSERT INTO users
                (name, role, avatar, status)
            VALUES
                (%s, %s, %s, %s)
            RETURNING
                id,
                name,
                role,
                avatar,
                status,
                created_at;
            """,
            (
                name,
                role,
                avatar,
                status
            )
        )

        user = cursor.fetchone()

        connection.commit()

        return dict(user)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# UPDATE USER
# ============================================================

@app.put("/users/{user_id}")
def update_user(
    user_id: int,
    name: str,
    role: str,
    avatar: str,
    status: bool
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            UPDATE users
            SET
                name = %s,
                role = %s,
                avatar = %s,
                status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                role,
                avatar,
                status,
                created_at;
            """,
            (
                name,
                role,
                avatar,
                status,
                user_id
            )
        )

        user = cursor.fetchone()

        if user is None:

            connection.rollback()

            return {
                "error": "User not found"
            }

        connection.commit()

        return dict(user)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DELETE USER
# ============================================================

@app.delete("/users/{user_id}")
def delete_user(user_id: int):

    connection = get_database_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM users
            WHERE id = %s
            RETURNING id;
            """,
            (user_id,)
        )

        deleted_user = cursor.fetchone()

        if deleted_user is None:

            connection.rollback()

            return {
                "error": "User not found"
            }

        connection.commit()

        return {
            "message": "User deleted successfully",
            "id": deleted_user[0]
        }

    finally:

        cursor.close()
        connection.close()         
        


# ============================================================
# GET SENSOR READINGS
# ============================================================

@app.get("/sensor-readings")
def get_sensor_readings():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id,
                device_id,
                temperature,
                humidity,
                power_watts,
                recorded_at
            FROM sensor_readings
            ORDER BY recorded_at DESC
            LIMIT 100;
            """
        )

        readings = cursor.fetchall()

        return [
            dict(reading)
            for reading in readings
        ]

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET LATEST SENSOR READING
# ============================================================

@app.get("/latest-reading")
def get_latest_reading():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                id,
                device_id,
                temperature,
                humidity,
                power_watts,
                recorded_at
            FROM sensor_readings
            ORDER BY recorded_at DESC
            LIMIT 1;
            """
        )

        reading = cursor.fetchone()

        if reading is None:

            return {
                "message": "No sensor readings found"
            }

        return dict(reading)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET ML RESULTS
# ============================================================

@app.get("/ml-results")
def get_ml_results():
    """
    Return ML prediction records.

    The ML save script may create ml_predictions without id,
    device_id, or created_at. This endpoint therefore checks which
    columns actually exist before querying them.
    """
    connection = None
    cursor = None

    try:
        connection = get_database_connection()

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        # Check the real columns in ml_predictions.
        cursor.execute(
            """
            SELECT column_name
            FROM information_schema.columns
            WHERE table_schema = 'public'
              AND table_name = 'ml_predictions'
            ORDER BY ordinal_position;
            """
        )

        existing_columns = {
            row["column_name"]
            for row in cursor.fetchall()
        }

        if not existing_columns:
            return {
                "error": "The ml_predictions table does not exist or has no columns.",
                "results": [],
            }

        # Only select columns that really exist.
        wanted_columns = [
            "id",
            "device_id",
            "temperature",
            "humidity",
            "ac_on",
            "lights_on",
            "tv_on",
            "actual_power_watts",
            "predicted_power_watts",
            "anomaly_status",
            "created_at",
            "recorded_at",
            "timestamp",
        ]

        selected = [
            column
            for column in wanted_columns
            if column in existing_columns
        ]

        if not selected:
            return {
                "error": "No supported ML result columns were found.",
                "available_columns": sorted(existing_columns),
                "results": [],
            }

        query = f"""
            SELECT {", ".join(selected)}
            FROM ml_predictions
            ORDER BY
                {("created_at DESC" if "created_at" in existing_columns
                   else "id DESC" if "id" in existing_columns
                   else "1")}
            LIMIT 100;
        """

        cursor.execute(query)
        results = cursor.fetchall()

        return [dict(result) for result in results]

    except Exception as error:
        # Return the actual database error as JSON so it can be
        # diagnosed instead of showing a blank HTTP 500 page.
        return {
            "error": str(error),
            "results": [],
        }

    finally:
        if cursor is not None:
            cursor.close()

        if connection is not None:
            connection.close()



# ============================================================
# AUTOMATIONS
# ============================================================

@app.on_event("startup")
def create_automations_table():
    """
    Create the PostgreSQL automations table if it does not exist.
    """

    connection = get_database_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS automations (
                id SERIAL PRIMARY KEY,
                name VARCHAR(150) NOT NULL,
                device_id INTEGER,
                trigger_type VARCHAR(50) NOT NULL,
                trigger_value VARCHAR(100),
                action VARCHAR(50) NOT NULL,
                schedule_time VARCHAR(10),
                status BOOLEAN DEFAULT TRUE,
                last_triggered TIMESTAMP NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                CONSTRAINT fk_automation_device
                    FOREIGN KEY (device_id)
                    REFERENCES devices(id)
                    ON DELETE SET NULL
            );
            """
        )

        connection.commit()

    finally:

        cursor.close()
        connection.close()


# ============================================================
# GET AUTOMATIONS
# ============================================================

@app.get("/automations")
def get_automations():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            SELECT
                a.id,
                a.name,
                a.device_id,
                d.name AS device_name,
                d.room AS device_room,
                a.trigger_type,
                a.trigger_value,
                a.action,
                a.schedule_time,
                a.status,
                a.last_triggered,
                a.created_at
            FROM automations a
            LEFT JOIN devices d
                ON d.id = a.device_id
            ORDER BY a.id DESC;
            """
        )

        automations = cursor.fetchall()

        return [
            dict(automation)
            for automation in automations
        ]

    finally:

        cursor.close()
        connection.close()


# ============================================================
# ADD AUTOMATION
# ============================================================

@app.post("/automations")
def add_automation(
    name: str,
    device_id: int | None = None,
    trigger_type: str = "Manual",
    trigger_value: str = "",
    action: str = "Turn ON",
    schedule_time: str | None = None,
    status: bool = True
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            INSERT INTO automations
                (
                    name,
                    device_id,
                    trigger_type,
                    trigger_value,
                    action,
                    schedule_time,
                    status
                )
            VALUES
                (%s, %s, %s, %s, %s, %s, %s)
            RETURNING
                id,
                name,
                device_id,
                trigger_type,
                trigger_value,
                action,
                schedule_time,
                status,
                last_triggered,
                created_at;
            """,
            (
                name,
                device_id,
                trigger_type,
                trigger_value,
                action,
                schedule_time,
                status
            )
        )

        automation = cursor.fetchone()

        connection.commit()

        return dict(automation)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# UPDATE AUTOMATION
# ============================================================

@app.put("/automations/{automation_id}")
def update_automation(
    automation_id: int,
    name: str,
    device_id: int | None = None,
    trigger_type: str = "Manual",
    trigger_value: str = "",
    action: str = "Turn ON",
    schedule_time: str | None = None,
    status: bool = True
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            UPDATE automations
            SET
                name = %s,
                device_id = %s,
                trigger_type = %s,
                trigger_value = %s,
                action = %s,
                schedule_time = %s,
                status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                device_id,
                trigger_type,
                trigger_value,
                action,
                schedule_time,
                status,
                last_triggered,
                created_at;
            """,
            (
                name,
                device_id,
                trigger_type,
                trigger_value,
                action,
                schedule_time,
                status,
                automation_id
            )
        )

        automation = cursor.fetchone()

        if automation is None:

            connection.rollback()

            return {
                "error": "Automation not found"
            }

        connection.commit()

        return dict(automation)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DELETE AUTOMATION
# ============================================================

@app.delete("/automations/{automation_id}")
def delete_automation(automation_id: int):

    connection = get_database_connection()

    try:

        cursor = connection.cursor()

        cursor.execute(
            """
            DELETE FROM automations
            WHERE id = %s
            RETURNING id;
            """,
            (automation_id,)
        )

        deleted_automation = cursor.fetchone()

        if deleted_automation is None:

            connection.rollback()

            return {
                "error": "Automation not found"
            }

        connection.commit()

        return {
            "message": "Automation deleted successfully",
            "id": deleted_automation[0]
        }

    finally:

        cursor.close()
        connection.close()


# ============================================================
# TOGGLE AUTOMATION STATUS
# ============================================================

@app.patch("/automations/{automation_id}/status")
def toggle_automation_status(
    automation_id: int,
    status: bool
):

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        cursor.execute(
            """
            UPDATE automations
            SET status = %s
            WHERE id = %s
            RETURNING
                id,
                name,
                status;
            """,
            (
                status,
                automation_id
            )
        )

        automation = cursor.fetchone()

        if automation is None:

            connection.rollback()

            return {
                "error": "Automation not found"
            }

        connection.commit()

        return dict(automation)

    finally:

        cursor.close()
        connection.close()


# ============================================================
# DASHBOARD SUMMARY
# ============================================================

@app.get("/dashboard-summary")
def dashboard_summary():

    connection = get_database_connection()

    try:

        cursor = connection.cursor(
            cursor_factory=RealDictCursor
        )

        # ----------------------------------------
        # Total devices
        # ----------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS total_devices
            FROM devices;
            """
        )

        total_devices = cursor.fetchone()["total_devices"]


        # ----------------------------------------
        # Active devices
        # ----------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS active_devices
            FROM devices
            WHERE status = TRUE;
            """
        )

        active_devices = cursor.fetchone()["active_devices"]


        # -------------------------
        # Current power
        # ----------------------------------------

        cursor.execute(
            """
            SELECT COALESCE(
                SUM(power_watts),
                0
            ) AS current_power
            FROM devices
            WHERE status = TRUE;
            """
        )

        current_power = cursor.fetchone()["current_power"]


        # ----------------------------------------
        # Anomalies
        # ----------------------------------------

        cursor.execute(
            """
            SELECT COUNT(*) AS anomaly_count
            FROM ml_predictions
            WHERE LOWER(
                anomaly_status::text
            ) IN (
                'anomaly',
                'true',
                '1'
            );
            """
        )

        anomaly_count = cursor.fetchone()["anomaly_count"]


        return {
            "total_devices": total_devices,
            "active_devices": active_devices,
            "current_power": float(current_power),
            "anomaly_count": anomaly_count,
        }

    finally:

        cursor.close()
        connection.close()


# ============================================================
# ENERGY PREDICTION
# ============================================================

@app.post("/predict-energy")
def predict_energy(
    temperature: float,
    humidity: float,
    ac_on: int,
    lights_on: int,
    tv_on: int,
):

    if energy_model is None:

        return {
            "error": "Energy prediction model is not loaded."
        }


    # Features must match the training order
    features = [[
        temperature,
        humidity,
        ac_on,
        lights_on,
        tv_on,
    ]]


    prediction = energy_model.predict(
        features
    )


    predicted_power = float(
        prediction[0]
    )


    return {
        "prediction_type": "Energy Prediction",
        "temperature": temperature,
        "humidity": humidity,
        "ac_on": ac_on,
        "lights_on": lights_on,
        "tv_on": tv_on,
        "predicted_power_watts": round(
            predicted_power,
            2
        ),
    }


# ============================================================
# ANOMALY DETECTION
# ============================================================

@app.post("/detect-anomaly")
def detect_anomaly(
    temperature: float,
    humidity: float,
    ac_on: int,
    lights_on: int,
    tv_on: int,
    power_watts: float,
):

    if anomaly_model is None:

        return {
            "error": "Anomaly detection model is not loaded."
        }


    # Features must match anomaly model training
    features = [[
        temperature,
        humidity,
        ac_on,
        lights_on,
        tv_on,
        power_watts,
    ]]


    prediction = anomaly_model.predict(
        features
    )


    prediction_value = int(
        prediction[0]
    )


    if prediction_value == -1:

        status = "Anomaly"

    else:

        status = "Normal"


    return {
        "prediction_type": "Anomaly Detection",
        "anomaly_status": status,
        "power_watts": power_watts,
    }


# ============================================================
# ML STATUS
# ============================================================

@app.get("/ml-status")
def ml_status():

    return {
        "energy_prediction": {
            "algorithm": "Linear Regression",
            "model_loaded": energy_model is not None,
        },

        "anomaly_detection": {
            "algorithm": "Isolation Forest",
            "model_loaded": anomaly_model is not None,
        },
    }


# ============================================================
# DATABASE STATUS
# ============================================================

@app.get("/database-status")
def database_status():

    try:

        connection = get_database_connection()

        cursor = connection.cursor()

        cursor.execute(
            "SELECT version();"
        )

        version = cursor.fetchone()[0]

        cursor.close()
        connection.close()

        return {
            "status": "connected",
            "database": "PostgreSQL",
            "version": version,
        }

    except Exception as error:

        return {
            "status": "disconnected",
            "error": str(error),
        }