def find_similar_evidence(transaction, evidence_samples, limit=3):
    scored_rows = []

    for _, row in evidence_samples.iterrows():
        score = 0
        if row["country"] == transaction["country"]:
            score += 2
        if row["channel"] == transaction["channel"]:
            score += 2
        if row["merchant_category"] == transaction["merchant_category"]:
            score += 3

        scored_rows.append((score, row))

    ranked = sorted(scored_rows, key=lambda item: item[0], reverse=True)
    rows = [row for score, row in ranked if score > 0][:limit]

    if not rows:
        return evidence_samples.head(1)

    return evidence_samples.loc[[row.name for row in rows]]
