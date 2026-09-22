🏠 AI Home Intelligence

AI-powered smart home monitoring, energy prediction and anomaly detection dashboard.

✨ Overview

AI Home Intelligence is a full-stack AI/ML smart home application that integrates smart-home data, machine learning, PostgreSQL, FastAPI, and Streamlit. It uses Linear Regression for energy consumption prediction and Isolation Forest for anomaly detection, with interactive device monitoring, analytics, alerts, automations, and AI-powered insights.

Main Features

🏠 Smart Home Dashboard

💡 Device monitoring & ON/OFF control

👤 User management

📊 Energy tracking & reports

🤖 Energy prediction

🚨 Anomaly detection

⚙️ Automations

🔔 Alerts

🏷️ Category management

🧠 AI Model Center

🧠 How It Works

📡 Home Data
     ↓
🐍 Python Processing
     ↓
🤖 ML Models
     ├── ⚡ Energy Prediction
     └── 🚨 Anomaly Detection
     ↓
🗄️ PostgreSQL
     ↓
🚀 FastAPI
     ↓
🎨 Streamlit Dashboard

🤖 Machine Learning

⚡ Energy Prediction

Algorithm: Linear Regression

Uses temperature, humidity and device states to predict power consumption.

🚨 Anomaly Detection

Algorithm: Isolation Forest

Detects unusual energy-consumption patterns.

🧰 Tech Stack

🐍 Python

🤖 Scikit-learn

📊 Pandas / NumPy

🚀 FastAPI

🎨 Streamlit

🗄️ PostgreSQL

📈 Plotly / Altair

💾 Joblib


🚀 Run the Project

1. Install dependencies

pip install -r requirements.txt

2. Configure PostgreSQL

3. Generate data

python src/generate_data.py

4. Save ML results

python src/save_ml_results.py

5. Start FastAPI

uvicorn backend.main:app --reload

Swagger:

http://127.0.0.1:8000/docs

6. Start Streamlit

http://localhost:8501

https://ai-home-intelligence.streamlit.app

streamlit run dashboard/app.py

📊 Dashboard

The application includes:

Home • Tracking • AI Insights • Automations • Alerts • Devices • Reports • Account • AI Model Center • Support • How It Works

🔄 Application Architecture

👤 User
 ↓
🎨 Streamlit
 ↓
🚀 FastAPI
 ↓
🗄️ PostgreSQL
 ↓
🤖 ML Results
 ↓
📊 Insights & Reports

🌟 Skills Demonstrated

Python • Machine Learning • FastAPI • REST APIs • PostgreSQL • SQL • Streamlit • Data Processing • Data Visualization • CRUD • Git/GitHub