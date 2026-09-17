"""
Model Serving (FastAPI)
=======================

FastAPI prediction endpoint for the credit risk model.

Endpoints
---------
GET  /health
POST /predict
POST /predict/batch
"""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Optional

import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parent.parent

MODEL_PATH = (
    PROJECT_ROOT
    / "artifacts"
    / "results"
    / "best_model.joblib"
)

# ---------------------------------------------------------------------------
# FastAPI app
# ---------------------------------------------------------------------------

app = FastAPI(
    title="Credit Risk Prediction API",
    description="Predicts credit default probability using a trained ML pipeline.",
    version="0.1.0",
)

# ---------------------------------------------------------------------------
# CORS
# ---------------------------------------------------------------------------
# Allows the React/Vite frontend running on localhost:5173
# to communicate with this FastAPI backend.

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Global model
# ---------------------------------------------------------------------------

_model = None


# ---------------------------------------------------------------------------
# Load model
# ---------------------------------------------------------------------------

@app.on_event("startup")
def load_model() -> None:
    """Load the trained model when the API starts."""
    global _model

    try:
        if not MODEL_PATH.exists():
            logger.warning(
                f"Model not found at: {MODEL_PATH}"
            )
            _model = None
            return

        _model = joblib.load(MODEL_PATH)

        logger.info(
            f"Model loaded successfully from: {MODEL_PATH}"
        )

    except Exception as exc:
        _model = None
        logger.exception(
            f"Failed to load model: {exc}"
        )


# ---------------------------------------------------------------------------
# Request schemas
# ---------------------------------------------------------------------------

class CreditApplication(BaseModel):
    """Credit application submitted by the frontend."""

    age: int = Field(
        ...,
        ge=18,
        description="Applicant age",
    )

    credit_amount: float = Field(
        ...,
        gt=0,
        description="Loan amount",
    )

    duration: int = Field(
        ...,
        ge=1,
        description="Loan duration in months",
    )

    employment_since: Optional[float] = Field(
        None,
        ge=0,
        description="Years at current job",
    )

    existing_credits: Optional[int] = Field(
        None,
        ge=0,
        description="Number of existing credits",
    )

    housing: Optional[str] = Field(
        None,
        description="Housing type: own, rent, free",
    )

    income: Optional[float] = Field(
        None,
        gt=0,
        description="Annual income",
    )

    purpose: Optional[str] = Field(
        None,
        description="Loan purpose",
    )

    class Config:
        json_schema_extra = {
            "example": {
                "age": 35,
                "credit_amount": 5000,
                "duration": 24,
                "employment_since": 4,
                "existing_credits": 1,
                "housing": "own",
                "income": 600000,
                "purpose": "car",
            }
        }


# ---------------------------------------------------------------------------
# Response schemas
# ---------------------------------------------------------------------------

class PredictionResponse(BaseModel):
    """Prediction returned by the API."""

    default_probability: float
    risk_category: str
    threshold: float
    prediction: int
    adverse_action_reasons: list[str]


class BatchRequest(BaseModel):
    """Batch prediction request."""

    applications: list[CreditApplication]


class BatchResponse(BaseModel):
    """Batch prediction response."""

    predictions: list[PredictionResponse]
    count: int


# ---------------------------------------------------------------------------
# Root endpoint
# ---------------------------------------------------------------------------

@app.get("/")
def root() -> dict:
    """Basic API information."""
    return {
        "message": "Credit Risk Prediction API is running",
        "docs": "/docs",
        "health": "/health",
        "predict": "/predict",
    }


# ---------------------------------------------------------------------------
# Health endpoint
# ---------------------------------------------------------------------------

@app.get("/health")
def health() -> dict:
    """Check API and model status."""

    return {
        "status": "healthy",
        "model_loaded": _model is not None,
        "model_path": str(MODEL_PATH),
    }


# ---------------------------------------------------------------------------
# Single prediction
# ---------------------------------------------------------------------------

@app.post(
    "/predict",
    response_model=PredictionResponse,
)
def predict(
    application: CreditApplication,
) -> PredictionResponse:
    """Score a single credit application."""

    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Check the model file.",
        )

    try:
        # Convert Pydantic object to dictionary
        data = application.model_dump()

        # Convert to DataFrame
        df = pd.DataFrame([data])

        logger.info(
            f"Prediction request received: {data}"
        )

        return _score_single(df)

    except HTTPException:
        raise

    except Exception as exc:
        logger.exception(
            f"Unexpected prediction error: {exc}"
        )

        raise HTTPException(
            status_code=500,
            detail=f"Prediction failed: {exc}",
        )


# ---------------------------------------------------------------------------
# Batch prediction
# ---------------------------------------------------------------------------

@app.post(
    "/predict/batch",
    response_model=BatchResponse,
)
def predict_batch(
    request: BatchRequest,
) -> BatchResponse:
    """Score multiple credit applications."""

    if _model is None:
        raise HTTPException(
            status_code=503,
            detail="Model not loaded. Check the model file.",
        )

    predictions = []

    for application in request.applications:

        data = application.model_dump()

        df = pd.DataFrame([data])

        predictions.append(
            _score_single(df)
        )

    return BatchResponse(
        predictions=predictions,
        count=len(predictions),
    )


# ---------------------------------------------------------------------------
# Scoring
# ---------------------------------------------------------------------------

DEFAULT_THRESHOLD = 0.35


def _score_single(
    df: pd.DataFrame,
) -> PredictionResponse:
    """Generate a prediction for one applicant."""

    try:

        # Ask trained model for probability
        probability = _model.predict_proba(df)[0, 1]

    except Exception as exc:

        logger.exception(
            f"Model prediction failed: {exc}"
        )

        raise HTTPException(
            status_code=422,
            detail=f"Prediction failed: {exc}",
        )

    probability = float(probability)

    # -----------------------------------------------------------------------
    # Prediction
    # -----------------------------------------------------------------------

    prediction = int(
        probability >= DEFAULT_THRESHOLD
    )

    # -----------------------------------------------------------------------
    # Risk category
    # -----------------------------------------------------------------------

    if probability < 0.15:
        category = "Low Risk"

    elif probability < 0.35:
        category = "Medium Risk"

    elif probability < 0.60:
        category = "High Risk"

    else:
        category = "Very High Risk"

    # -----------------------------------------------------------------------
    # Reasons
    # -----------------------------------------------------------------------

    reasons = _get_adverse_reasons(
        df,
        probability,
    )

    return PredictionResponse(
        default_probability=round(
            probability,
            4,
        ),
        risk_category=category,
        threshold=DEFAULT_THRESHOLD,
        prediction=prediction,
        adverse_action_reasons=reasons,
    )


# ---------------------------------------------------------------------------
# Explainability / reasons
# ---------------------------------------------------------------------------

def _get_adverse_reasons(
    df: pd.DataFrame,
    probability: float,
) -> list[str]:
    """
    Generate simple rule-based reasons.

    NOTE:
    These are NOT true model explanations.
    A production system should use a proper explainability
    method such as SHAP or model coefficients.
    """

    reasons = []

    row = df.iloc[0]

    # Loan amount
    credit_amount = row.get("credit_amount")

    if pd.notna(credit_amount):

        if credit_amount > 10000:
            reasons.append(
                "High loan amount requested"
            )

    # Loan duration
    duration = row.get("duration")

    if pd.notna(duration):

        if duration > 36:
            reasons.append(
                "Long loan duration"
            )

    # Age
    age = row.get("age")

    if pd.notna(age):

        if age < 25:
            reasons.append(
                "Young applicant with potentially limited credit history"
            )

    # Existing credits
    existing_credits = row.get(
        "existing_credits"
    )

    if pd.notna(existing_credits):

        if existing_credits > 3:
            reasons.append(
                "High number of existing credits"
            )

    # Loan-to-income ratio
    income = row.get("income")

    if (
        pd.notna(income)
        and pd.notna(credit_amount)
        and income > 0
    ):

        loan_income_ratio = (
            credit_amount / income
        )

        if loan_income_ratio > 0.30:
            reasons.append(
                "Loan amount is high relative to reported income"
            )

    # Fallback
    if (
        not reasons
        and probability > DEFAULT_THRESHOLD
    ):
        reasons.append(
            "Combined model risk factors exceed the prediction threshold"
        )

    return reasons