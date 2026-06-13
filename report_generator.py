def generate_report(transaction, rule_result, ml_score, decision, evidence):
    lines = [
        "[FraudInvestigator Lite 조사 리포트 초안]",
        "",
        f"- 거래 ID: {transaction['transaction_id']}",
        f"- 고객 ID: {transaction['customer_id']}",
        f"- 거래 시각: {transaction['transaction_time']}",
        f"- 거래 금액: {int(transaction['amount']):,} {transaction['currency']}",
        f"- 국가/채널/업종: {transaction['country']} / {transaction['channel']} / {transaction['merchant_category']}",
        "",
        "[탐지 이후 조사 신호]",
        f"- Rule score: {rule_result['score']}",
        f"- ML fraud score: {ml_score:.2f}",
        f"- 분류: {decision}",
        "",
        "[Rule 근거]",
    ]

    lines.extend(f"- {reason}" for reason in rule_result["reasons"])

    if decision == "Review" and not evidence.empty:
        lines.extend(["", "[참고 가능한 유사 사례 샘플]"])
        for _, row in evidence.iterrows():
            lines.append(f"- {row['case_id']}: {row['signal']} / {row['investigation_note']}")

    lines.extend(
        [
            "",
            "[조사자 확인 필요 사항]",
            "- 본인 거래 여부, 최근 기기/접속 환경 변경, 해외 이용 정황을 확인합니다.",
            "- 본 초안은 조사 업무 지원용이며 최종 판단은 조사자가 수행합니다.",
            "- 본 MVP는 샘플 데이터 기반 시연 앱이며 실제 내부 FDS/API/DB와 연동되지 않습니다.",
        ]
    )

    return "\n".join(lines)
