from fastapi import FastAPI, HTTPException
import uvicorn
import pandas as pd
import sqlite3
import joblib
import os

# Initialize FastAPI app
app = FastAPI()

# Set paths dynamically
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "fraud_detection_xgboost.pkl")
DB_PATH = os.path.join(BASE_DIR, "test_logs.db")

# Load the trained model
try:
    with open(MODEL_PATH, "rb") as file:
        model = joblib.load(file)
    print("✅ Model loaded successfully!")
except Exception as e:
    print(f"❌ Error loading model: {e}")
    model = None

# Initialize Database
def init_db():
    conn = sqlite3.connect(DB_PATH, check_same_thread=False)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
                 id INTEGER PRIMARY KEY AUTOINCREMENT, 
                 input TEXT, 
                 prediction INTEGER)''')
    conn.commit()
    conn.close()

init_db()  # Initialize database on API startup

@app.get("/")
def home():
    return {"message": "Fraud Detection API is running!"}

@app.post("/predict/")
def predict(data: dict):
    try:
        # Extract features
        features = ["step", "amount", "isFlaggedFraud", "isMerchant", "amount_ratio", "type_encoded"]
        df = pd.DataFrame([data])
        df = df[features]  # Ensure correct feature order

        prediction = model.predict(df)

        # Log prediction in the database
        conn = sqlite3.connect(DB_PATH, check_same_thread=False)
        c = conn.cursor()
        c.execute("INSERT INTO logs (input, prediction) VALUES (?, ?)", (str(data), int(prediction[0])))
        conn.commit()
        conn.close()

        return {"fraud_prediction": int(prediction[0])}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

# Run the API
if __name__ == "__main__":
    PORT = int(os.getenv("PORT", 8000))  # Get PORT from environment, default to 8000
    uvicorn.run(app, host="0.0.0.0", port=PORT)
