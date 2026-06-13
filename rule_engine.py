from datetime import datetime


def calculate_rule_score(transaction):
    score = 0
    reasons = []

    amount = float(transaction["amount"])
    avg_amount = float(transaction["avg_30d_amount"])
    account_age_days = int(transaction["account_age_days"])
    country = transaction["country"]
    channel = transaction["channel"]
    merchant_category = transaction["merchant_category"]
    tx_time = datetime.strptime(transaction["transaction_time"], "%Y-%m-%d %H:%M:%S")

    if amount >= avg_amount * 5:
        score += 35
        reasons.append("최근 30일 평균 거래금액 대비 5배 이상")

    if amount >= 1_000_000:
        score += 25
        reasons.append("고액 거래 기준 초과")

    if country != "KR":
        score += 20
        reasons.append("해외 거래")

    if tx_time.hour < 6:
        score += 10
        reasons.append("심야 시간대 거래")

    if account_age_days < 90:
        score += 10
        reasons.append("신규 또는 단기 이용 계정")

    if merchant_category in {"digital_goods", "travel"}:
        score += 10
        reasons.append("주의가 필요한 업종 패턴")

    if channel == "web" and amount >= 1_000_000:
        score += 5
        reasons.append("웹 채널 고액 거래")

    if not reasons:
        reasons.append("주요 Rule 이상 신호 낮음")

    return {"score": min(score, 100), "reasons": reasons}
