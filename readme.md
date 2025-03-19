# 🚀 Finance Fraud Detection API

## 📌 Overview
This is a **FastAPI**-powered machine learning API for detecting fraudulent transactions. It is built using **XGBoost** and logs predictions in a **SQLite database**. The API is deployed on **Render** and can be accessed externally.

---

## ⚙️ Features
✅ **Fraud Detection**: Predicts if a transaction is fraudulent (1) or not (0).  
✅ **SQLite Logging**: Each request and prediction is logged for future analysis.  
✅ **FastAPI**: Lightweight and efficient REST API.  
✅ **Deployed on Render**: Accessible online via a public endpoint.  

---

## 🛠️ Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/yourusername/fraud-detection-api.git
cd fraud-detection-api
```

### **2️⃣ Create a Virtual Environment**
```bash
python -m venv venv
source venv/bin/activate  # For macOS/Linux
venv\Scripts\activate    # For Windows
```

### **3️⃣ Install Dependencies**
```bash
pip install -r requirements.txt
```

### **4️⃣ Run the API Locally**
```bash
uvicorn final_api:app --host 0.0.0.0 --port 8000
```

Once running, open in your browser:
```
http://localhost:8000/
```

---

## 🖥️ API Endpoints
### **🔹 Health Check**
```http
GET /
```
_Response:_
```json
{"message": "Fraud Detection API is running!"}
```

### **🔹 Predict Fraudulent Transaction**
```http
POST /predict/
```
#### **🔹 Request Body (JSON Format):**
```json
{
    "step": 1,
    "amount": 1000,
    "isFlaggedFraud": 0,
    "isMerchant": 1,
    "amount_ratio": 0.001,
    "type_encoded": 2
}
```
#### **🔹 Response:**
```json
{
    "fraud_prediction": 0
}
```

---

## 📊 **SQLite Logging**
All predictions are logged in `logs.db`. To view logs:
1. Open `logs.db` in **DB Browser for SQLite**.
2. Run the query:
```sql
SELECT * FROM logs;
```
3. View all logged API requests and predictions.

---

## 🌍 Deployment on Render
### **1️⃣ Deploying via GitHub**
- Push the repository to GitHub.
- Connect GitHub repo to Render.
- Set the **Start Command** as:
```bash
uvicorn final_api:app --host 0.0.0.0 --port 8000
```
- Deploy & test the API!

### **2️⃣ Render API URL**
Replace `your-api-url` with the actual Render deployment URL:
```bash
API_URL = "https://your-api-url.onrender.com/predict/"
```

---

## 📝 Future Improvements
✅ Enhance fraud detection model with additional features.  
✅ Implement authentication & rate limiting.  
✅ Add frontend for real-time transaction analysis.  

---

## 📄 License
This project is licensed under **MIT License**. Feel free to use and modify.  

---

## 🤝 Contributing
Pull requests are welcome! If you find issues, open an issue in the repository.

---

## 📩 Contact
For any queries, reach out via [GitHub Issues](https://github.com/yourusername/fraud-detection-api/issues).

