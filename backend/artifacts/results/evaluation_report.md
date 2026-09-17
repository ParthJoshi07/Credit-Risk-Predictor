# Credit Risk Pipeline - Evaluation Report

## Model Comparison

| Model | ROC-AUC | Recall | F1 |
|-------|---------|--------|----|
| LogisticRegression ** | 0.787 +/- 0.020 | 0.713 | 0.606 |
| GradientBoosting | 0.769 +/- 0.013 | 0.447 | 0.513 |

**Best Model**: LogisticRegression

## Cost-Sensitive Threshold Tuning

- **Optimal Threshold**: 0.26
- **Minimum Cost**: $537
- **Cost Ratio**: FN=10x, FP=1x

## Classification Report (at optimal threshold)

| Class | Precision | Recall | F1 | Support |
|-------|-----------|--------|----|---------|
| 0 | 0.951 | 0.476 | 0.634 | 700 |
| 1 | 0.435 | 0.943 | 0.596 | 300 |

## Top Features (SHAP)

| Rank | Feature | Mean |SHAP| |
|------|---------|-------------|
| 1 | num__credit_amount | 0.5015 |
| 2 | cat__checking_status_no checking | 0.4922 |
| 3 | num__duration | 0.4044 |
| 4 | cat__credit_history_critical/other existing credit | 0.3634 |
| 5 | num__installment_commitment | 0.3112 |
| 6 | num__loan_burden | 0.3065 |
| 7 | cat__checking_status_<0 | 0.2695 |
| 8 | cat__purpose_new car | 0.2337 |
| 9 | cat__savings_status_<100 | 0.2260 |
| 10 | cat__personal_status_male single | 0.2242 |

## Artifacts

- `artifacts/figures/precision_recall_curve.png`
- `artifacts/figures/confusion_matrix.png`
- `artifacts/figures/shap_importance.png`
- `artifacts/results/best_model.joblib`