def get_ml_score(transaction):
    if "ml_fraud_score" in transaction:
        return float(transaction["ml_fraud_score"])

    amount = float(transaction["amount"])
    avg_amount = float(transaction["avg_30d_amount"])
    ratio = amount / max(avg_amount, 1)
    return min(0.95, 0.1 + ratio * 0.08)
