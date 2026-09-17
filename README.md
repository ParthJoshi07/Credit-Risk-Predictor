Credit Risk Predictor

A full-stack machine learning application that predicts the credit risk of a loan applicant based on financial and personal attributes.

The project combines a trained machine learning model with a FastAPI backend and a React-based frontend to provide real-time credit risk predictions through an interactive web interface.

Tech Stack

Frontend: React.js, Vite, JavaScript, HTML, CSS

Backend: Python, FastAPI

Machine Learning: Scikit-learn, Pandas, NumPy

Model Serving: Joblib

API: REST API

Project Structure

Credit-Risk-Predictor/
├── frontend/          # React + Vite web application
├── backend/           # ML pipeline and FastAPI service
├── artifacts/         # Trained model and generated artifacts
└── README.md

Key Features

Credit risk prediction using a trained ML model

Feature engineering and data preprocessing

FastAPI-based prediction API

Interactive React frontend

Real-time communication between frontend and backend

Input validation and feature mapping

Modular ML pipeline for training and inference

How It Works

User Input
    ↓
React Frontend
    ↓
FastAPI Backend
    ↓
Data Validation & Feature Engineering
    ↓
Trained ML Model
    ↓
Credit Risk Prediction
    ↓
Result Displayed to User

Setup

Backend

cd backend
pip install -r requirements.txt
uvicorn src.serve:app --reload --port 8000

Frontend

cd frontend
npm install
npm run dev

The frontend connects to the FastAPI backend to send applicant data and display the predicted credit risk.

Project Goal

The goal of this project is to demonstrate how a machine learning model can be integrated into a production-style full-stack application, from data preprocessing and feature engineering to model serving and a user-facing web interface.
