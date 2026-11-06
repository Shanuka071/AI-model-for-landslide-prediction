# AI-Based Application for Landslide and Flood Prediction System

An end-to-end machine learning web application designed to predict landslide and flood risks using meteorological data, featuring real-time district-level risk alerts and data visualization.

---

## 🚀 Features
* **Predictive Modeling:** Utilizes a Reinforcement Learning model trained on daily and 7-day cumulative rainfall data.
* **High Accuracy:** Achieves an overall multi-hazard prediction accuracy of **75.14%**.
* **Live Alerts:** Generates dynamic, district-level risk warnings based on real-time weather inputs.
* **Interactive UI:** Built with Streamlit for a clean, user-friendly, and dark-themed visualization experience.

---

## 🛠️ Tech Stack
Backend & Machine Learning:
  * Python
  * Pandas, NumPy
  * Scikit-learn
  * OpenAI Gym (Reinforcement Learning)
  * Flask API
* **Frontend & UI:** 
  * Streamlit
  * HTML / CSS / JavaScript

---

## 📂 Project Structure
```text
├── app.py                 # Main Streamlit application frontend
├── backend/               # Flask API and server-side logic
│   ├── app.py             # Flask application routes
│   └── model.pkl          # Trained machine learning model
├── model/                 # Training and RL model scripts (OpenAI Gym)
├── data/                  # Historical meteorological datasets
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation

👥 Authors & Collaborators

This project is co-developed and maintained by:
Shanuka -Shanuka071
Diluni Senanayake-Dilunis



