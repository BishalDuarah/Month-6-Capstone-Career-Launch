# Month-6-Capstone-Career-Launch
# 🏠 Real Estate Price Prediction System

A full-stack Machine Learning project that predicts real estate prices based on user inputs, with a production-ready architecture including API, monitoring, and frontend.

---

## 🚀 Features

- 📊 ML model with preprocessing + hyperparameter tuning (GridSearchCV)
- ⚡ FastAPI backend for real-time predictions
- 🐳 Dockerized backend
- 📈 Monitoring using Prometheus
- 📊 Visualization using Grafana
- ⚛️ React (Vite) frontend for user interaction

---

## 🧠 Tech Stack

### 🔹 Machine Learning
- Python
- scikit-learn
- Pandas, NumPy

### 🔹 Backend
- FastAPI
- Uvicorn

### 🔹 Frontend
- React (Vite)
- Axios

### 🔹 DevOps & Monitoring
- Docker
- Prometheus
- Grafana

---

## 📁 Project Structure
Capstone Project/
│
├── ml-pipeline/
│ ├── train.py
│ ├── preprocess.py
│ └── data/
│
├── backend/
│ ├── main.py
│ ├── services/
│ ├── model/
│ ├── Dockerfile
│ └── prometheus.yml
│
├── frontend/
│ ├── src/
│ ├── package.json
│
└── README.md

---

## Backend Setup
cd backend
python -m venv venv
venv\Scripts\activate   # Windows
pip install -r requirements.txt

uvicorn main:app --host 0.0.0.0 --port 8000

## Frontend Setup
cd frontend
npm install
npm run dev

## Run with Docker
docker build -t real-estate-api .
docker run -p 8000:8000 real-estate-api

## Monitoring
### Prometheus
docker run -d -p 9090:9090 \
--name prometheus \
-v "PATH_TO/prometheus.yml:/etc/prometheus/prometheus.yml" \
prom/prometheus

### Grafana
docker run -d -p 3000:3000 --name grafana grafana/grafana





