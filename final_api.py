from fastapi import FastAPI, HTTPException
import subprocess
import pandas as pd
import sqlite3
import os
import joblib

# Define base directory (for Render or local)
BASE_DIR = os.getcwd()

# Load Model
MODEL_PATH = os.path.join(BASE_DIR, "fraud_detection_xgboost.pkl")
try:
    model = joblib.load(MODEL_PATH)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Initialize FastAPI App
app = FastAPI()

# Database Connection
DB_PATH = os.path.join(BASE_DIR, "test_logs.db")
try:
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, input TEXT, prediction INTEGER)''')
    conn.commit()
    print("✅ Database connected and table initialized!")
except Exception as e:
    print(f"❌ Error setting up the database: {e}")

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        # Define required features
        features = ["step", "amount", "isFlaggedFraud", "isMerchant", "amount_ratio", "type_encoded"]

        df = pd.DataFrame([data])
        df = df[features]  # Ensure correct feature order

        prediction = model.predict(df)

        # Save to database
        c.execute("INSERT INTO logs (input, prediction) VALUES (?, ?)", (str(data), int(prediction[0])))
        conn.commit()

        return {"fraud_prediction": int(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Start the API by running uvicorn as a subprocess
subprocess.Popen(["uvicorn", "final_api:app", "--host", "0.0.0.0", "--port", "8001"])
