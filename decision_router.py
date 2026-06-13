def route_decision(rule_score, ml_score):
    if rule_score >= 70 or ml_score >= 0.85:
        return "Danger"

    if rule_score >= 35 or ml_score >= 0.55:
        return "Review"

    return "Clean"
