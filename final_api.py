from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import sqlite3
import joblib
import os

# Load Model
MODEL_PATH = "/kaggle/working/fraud_detection_xgboost.pkl"
try:
    with open(MODEL_PATH, "rb") as file:
        model = joblib.load(file)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Initialize FastAPI App
app = FastAPI()

# Database Connection
DB_PATH = "/kaggle/working/test_logs.db"
conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, input TEXT, prediction INTEGER)''')
conn.commit()

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

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
