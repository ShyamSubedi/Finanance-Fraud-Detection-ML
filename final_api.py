from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import sqlite3
import joblib
import os

# Load Model
MODEL_PATH = "fraud_detection_xgboost.pkl"
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
DB_PATH = "logs.db"
conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS logs (id INTEGER PRIMARY KEY, amount REAL, prediction INTEGER)''')
conn.commit()

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        # Extract amount from request
        amount = data.get("amount", None)
        if amount is None:
            raise HTTPException(status_code=400, detail="Amount is required for prediction.")

        # Automatically set default or calculated feature values
        transaction_data = {
            "step": 1,  # Default placeholder value
            "amount": amount,  # Provided by user
            "isFlaggedFraud": 0,  # Assume transaction is not flagged initially
            "isMerchant": 1,  # Assume merchant transaction
            "amount_ratio": amount / 100000 if amount > 0 else 0.00001,  # Example ratio calculation
            "type_encoded": 2  # Default transaction type encoding
        }

        # Convert to DataFrame
        df = pd.DataFrame([transaction_data])

        # Make prediction
        prediction = model.predict(df)[0]

        # Log request to SQLite
        cursor.execute("INSERT INTO logs (amount, prediction) VALUES (?, ?)", (amount, int(prediction)))
        conn.commit()

        return {"fraud_prediction": int(prediction)}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=PORT)
