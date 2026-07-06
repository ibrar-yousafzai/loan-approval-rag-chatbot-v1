import joblib
import numpy as np

model = joblib.load('loan_approval_rf_model.pkl')

FEATURE_ORDER = [
    'no_of_dependents', 'education', 'self_employed', 'income_annum',
    'loan_amount', 'loan_term', 'cibil_score', 'residential_assets_value',
    'commercial_assets_value', 'luxury_assets_value', 'bank_asset_value'
]

def predict_loan(data: dict):
    row = [data[col] for col in FEATURE_ORDER]
    X = np.array(row).reshape(1, -1)
    prediction = model.predict(X)[0]
    probability = model.predict_proba(X)[0]
    return prediction, probability

def explain_prediction(data: dict, prediction: int):
    """
    Reasons are now aligned with the ACTUAL prediction, not independent checks.
    """
    reasons = []

    cibil_ok = data['cibil_score'] >= 650
    income_ok = data['income_annum'] >= 200000  # realistic minimum based on dataset scale
    ratio_ok = data['income_annum'] / max(data['loan_amount'], 1) >= 0.3
    total_assets = (data['residential_assets_value'] + data['commercial_assets_value'] +
                     data['luxury_assets_value'] + data['bank_asset_value'])
    assets_ok = total_assets >= data['loan_amount']

    if prediction == 1:
        # Approved - list what worked in their favor
        if cibil_ok: reasons.append("Your CIBIL score is healthy (650+).")
        if income_ok: reasons.append("Your annual income is within a realistic, strong range.")
        if ratio_ok: reasons.append("Your income comfortably supports the requested loan amount.")
        if assets_ok: reasons.append("Your assets provide good backing for the loan.")
        if not reasons:
            reasons.append("Overall, your combined profile met our approval criteria.")
    else:
        # Rejected - list what likely worked against them
        if not cibil_ok: reasons.append("Your CIBIL score is below 650, which lowers approval chances.")
        if not income_ok: reasons.append("Your annual income is quite low compared to typical approved applicants.")
        if not ratio_ok: reasons.append("Your income is low relative to the loan amount requested.")
        if not assets_ok: reasons.append("Your total assets are lower than the requested loan amount.")
        if not reasons:
            reasons.append("Based on the overall combination of your details, our model predicts a lower approval likelihood, even though individual factors look reasonable — the model weighs all factors together, and low absolute income is a strong factor here.")

    return reasons

def get_suggestions(data: dict):
    suggestions = []

    if data['cibil_score'] < 650:
        suggestions.append("Work on improving your CIBIL score above 650 before reapplying.")
    if data['income_annum'] < 200000:
        suggestions.append("Your income is quite low for this loan amount — increasing verifiable income would help significantly.")
    ratio = data['income_annum'] / max(data['loan_amount'], 1)
    if ratio < 0.3:
        suggestions.append("Consider requesting a smaller loan amount relative to your income.")
    total_assets = (data['residential_assets_value'] + data['commercial_assets_value'] +
                     data['luxury_assets_value'] + data['bank_asset_value'])
    if total_assets < data['loan_amount']:
        suggestions.append("Adding more collateral/assets could strengthen your application.")

    if not suggestions:
        suggestions.append("Your profile looks strong on paper — if rejected, the model may be weighing a combination of factors not fully captured by these individual checks.")

    return suggestions