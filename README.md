# 💳 Credit Risk Predictor

A **full-stack machine learning application** designed to predict the **credit risk of loan applicants** using financial and personal attributes.

The project integrates a trained **Machine Learning model** with a **FastAPI REST API** and an interactive **React.js frontend**, enabling users to enter applicant information and receive **real-time credit risk predictions**.

---

## 🚀 Tech Stack

| Layer                | Technologies                          |
| -------------------- | ------------------------------------- |
| **Frontend**         | React.js, Vite, JavaScript, HTML, CSS |
| **Backend**          | Python, FastAPI                       |
| **Machine Learning** | Scikit-learn, Pandas, NumPy           |
| **Model Serving**    | Joblib                                |
| **API Architecture** | REST API                              |

---

## 📁 Project Structure

```text
Credit-Risk-Predictor/
│
├── frontend/          # React + Vite web application
│
├── backend/           # Python ML pipeline & FastAPI service
│
├── artifacts/         # Trained models and generated artifacts
│
└── README.md          # Project documentation
```

---

## ✨ Key Features

* 🤖 **Machine Learning Prediction** — Predicts applicant credit risk using a trained ML model.
* ⚙️ **Feature Engineering** — Processes and transforms raw applicant information into model-ready features.
* 🚀 **FastAPI Backend** — Provides a fast REST API for serving predictions.
* 💻 **Interactive Frontend** — React-based interface for entering applicant information and viewing results.
* ⚡ **Real-Time Predictions** — Sends applicant data to the backend and returns predictions instantly.
* ✅ **Input Validation** — Validates incoming data before passing it to the prediction pipeline.
* 🔄 **Feature Mapping** — Converts frontend inputs into the exact feature format required by the trained model.
* 🧩 **Modular Architecture** — Separates the frontend, API, ML pipeline, and model artifacts for easier development and maintenance.

---

## 🔄 How It Works

```text
┌─────────────────────┐
│     User Input      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│   React Frontend    │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│    FastAPI API      │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Input Validation &  │
│ Feature Engineering │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│  Trained ML Model   │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Credit Risk Result  │
└──────────┬──────────┘
           ↓
┌─────────────────────┐
│ Display Prediction  │
└─────────────────────┘
```

The user enters their financial information through the **React frontend**. The data is sent to the **FastAPI backend**, where it is validated and
