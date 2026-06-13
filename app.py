import pandas as pd
import streamlit as st


st.set_page_config(
    page_title="FraudInvestigator Lite",
    page_icon="FI",
    layout="wide",
    initial_sidebar_state="expanded",
)


DEMO_CASES = [
    {
        "case_title": "Case 01. 해외 심야 고액 결제",
        "demo_point": "Danger 케이스: Rule과 ML이 모두 강한 위험 신호를 보이는 거래",
        "transaction_id": "TX-9001",
        "customer_id": "C-1842",
        "customer_segment": "급여 이체 고객",
        "transaction_time": "2026-06-14 02:18:43",
        "amount": 4_850_000,
        "currency": "KRW",
        "country": "SG",
        "channel": "mobile",
        "merchant": "Global Travel Hub",
        "merchant_category": "travel",
        "merchant_risk": "High",
        "device_status": "신규 기기",
        "account_age_days": 38,
        "past_30d_tx_count": 7,
        "avg_30d_amount": 210_000,
        "rule_score": 92,
        "ml_fraud_score": 0.94,
        "triggered_rules": [
            "최근 30일 평균 거래금액 대비 23.1배",
            "해외 거래 + 심야 시간대",
            "신규 기기에서 고액 결제",
            "고위험 가맹점 카테고리",
        ],
        "risk_evidence": [
            "고객의 최근 거래는 국내 생활 업종 중심이며 해외 고액 결제 이력이 없음",
            "거래 시각이 평소 활동 시간대와 다르고 신규 기기 접속이 동반됨",
        ],
        "normal_evidence": [
            "여행 업종은 실제 해외 이용 가능성이 존재하므로 출국/예약 여부 확인 필요",
        ],
        "similar_cases": [
            "해외 여행 업종 고액 결제 후 본인 미사용 확인 사례",
            "신규 기기 등록 직후 심야 결제가 발생한 계정 탈취 의심 사례",
        ],
        "customer_questions": [
            "해당 시간에 싱가포르 또는 해외 여행 관련 결제를 직접 진행하셨나요?",
            "최근 휴대폰 변경 또는 신규 기기 등록을 하셨나요?",
        ],
    },
    {
        "case_title": "Case 02. Rule은 높지만 ML은 중간",
        "demo_point": "Review 케이스: Rule/ML 판단 충돌을 조사자가 근거로 확인하는 흐름",
        "transaction_id": "TX-9002",
        "customer_id": "C-2705",
        "customer_segment": "소상공인 고객",
        "transaction_time": "2026-06-14 22:41:09",
        "amount": 1_240_000,
        "currency": "KRW",
        "country": "KR",
        "channel": "web",
        "merchant": "Office Device Market",
        "merchant_category": "electronics",
        "merchant_risk": "Medium",
        "device_status": "기존 기기",
        "account_age_days": 860,
        "past_30d_tx_count": 41,
        "avg_30d_amount": 170_000,
        "rule_score": 63,
        "ml_fraud_score": 0.57,
        "triggered_rules": [
            "최근 평균 대비 7.3배 고액 거래",
            "야간 시간대 웹 결제",
            "전자제품 업종의 금액 급증",
        ],
        "risk_evidence": [
            "평소 소액·반복 거래 패턴 대비 단일 결제 금액이 큼",
            "웹 채널에서 야간 고액 결제가 발생함",
        ],
        "normal_evidence": [
            "기존 기기에서 발생했고 계정 사용 기간이 길어 계정 신뢰도는 낮지 않음",
            "소상공인 고객 특성상 업무용 장비 구매 가능성이 존재함",
        ],
        "similar_cases": [
            "사업자 고객의 업무용 전자기기 구매로 정상 확인된 사례",
            "웹 채널 고액 결제 후 고객 확인으로 정상 승인된 조사 사례",
        ],
        "customer_questions": [
            "업무용 전자기기 또는 사무 장비 구매 목적의 결제가 맞나요?",
            "결제 가맹점과 주문 내역을 확인하실 수 있나요?",
        ],
    },
    {
        "case_title": "Case 03. ML은 높지만 Rule은 중간",
        "demo_point": "Review 케이스: 정형 Rule이 놓칠 수 있는 패턴을 ML 신호로 보완",
        "transaction_id": "TX-9003",
        "customer_id": "C-3920",
        "customer_segment": "비대면 주거래 고객",
        "transaction_time": "2026-06-14 16:07:55",
        "amount": 680_000,
        "currency": "KRW",
        "country": "KR",
        "channel": "mobile",
        "merchant": "Digital Voucher Store",
        "merchant_category": "digital_goods",
        "merchant_risk": "High",
        "device_status": "기존 기기",
        "account_age_days": 190,
        "past_30d_tx_count": 12,
        "avg_30d_amount": 92_000,
        "rule_score": 48,
        "ml_fraud_score": 0.81,
        "triggered_rules": [
            "평균 대비 7.4배 거래",
            "디지털 상품권 업종",
            "고위험 가맹점군",
        ],
        "risk_evidence": [
            "디지털 상품권은 피해금 회수 가능성이 낮아 조사 우선순위가 높음",
            "금액은 Danger 기준 미만이지만 고객 평균 대비 급증",
        ],
        "normal_evidence": [
            "국내 거래이며 기존 기기에서 발생해 일부 정상 가능성이 존재함",
        ],
        "similar_cases": [
            "상품권 구매 후 즉시 환금이 확인된 의심 사례",
            "모바일 채널 디지털 상품 반복 구매로 Review 분류된 사례",
        ],
        "customer_questions": [
            "상품권 구매 목적과 수령자를 확인해주실 수 있나요?",
            "최근 문자, 메신저, 원격 제어 앱 설치 요청을 받은 적이 있나요?",
        ],
    },
    {
        "case_title": "Case 04. 정상 가능성이 높은 생활 거래",
        "demo_point": "Clean 케이스: 조사 우선순위를 낮춰 불필요한 고객 불편을 줄이는 흐름",
        "transaction_id": "TX-9004",
        "customer_id": "C-1188",
        "customer_segment": "장기 이용 고객",
        "transaction_time": "2026-06-14 12:26:30",
        "amount": 82_000,
        "currency": "KRW",
        "country": "KR",
        "channel": "mobile",
        "merchant": "Local Mart",
        "merchant_category": "groceries",
        "merchant_risk": "Low",
        "device_status": "기존 기기",
        "account_age_days": 1440,
        "past_30d_tx_count": 58,
        "avg_30d_amount": 76_000,
        "rule_score": 14,
        "ml_fraud_score": 0.09,
        "triggered_rules": [
            "주요 Rule 이상 신호 낮음",
            "평소 금액·업종·채널과 유사",
        ],
        "risk_evidence": [
            "특이 위험 근거 없음",
        ],
        "normal_evidence": [
            "국내 생활 업종에서 평소 평균 금액과 유사한 거래",
            "기존 기기와 평소 이용 채널에서 발생",
        ],
        "similar_cases": [],
        "customer_questions": [
            "추가 고객 확인 질문 생성 대상 아님",
        ],
    },
    {
        "case_title": "Case 05. 현금 인출 급증",
        "demo_point": "Danger 케이스: 비대면 결제가 아닌 ATM/현금화 패턴도 조사 큐에 포함",
        "transaction_id": "TX-9005",
        "customer_id": "C-5066",
        "customer_segment": "시니어 고객",
        "transaction_time": "2026-06-14 09:12:17",
        "amount": 3_000_000,
        "currency": "KRW",
        "country": "KR",
        "channel": "atm",
        "merchant": "ATM Withdrawal",
        "merchant_category": "cash_withdrawal",
        "merchant_risk": "Medium",
        "device_status": "카드 거래",
        "account_age_days": 2210,
        "past_30d_tx_count": 4,
        "avg_30d_amount": 120_000,
        "rule_score": 86,
        "ml_fraud_score": 0.88,
        "triggered_rules": [
            "최근 평균 대비 25배 현금 인출",
            "단기 거래 빈도 낮은 고객의 갑작스러운 고액 인출",
            "현금화 가능성이 높은 채널",
        ],
        "risk_evidence": [
            "평소 거래 빈도가 낮은 고객에게서 고액 현금 인출이 발생",
            "현금 인출은 피해 발생 시 추적·회수가 어렵기 때문에 우선 확인 필요",
        ],
        "normal_evidence": [
            "국내 거래이며 장기 이용 고객이라는 정상 가능성 근거가 일부 존재함",
        ],
        "similar_cases": [
            "보이스피싱 유도 후 ATM 고액 인출이 발생한 조사 사례",
            "시니어 고객의 단기 현금 인출 급증으로 우선 확인된 사례",
        ],
        "customer_questions": [
            "최근 수사기관, 금융기관, 지인을 사칭한 현금 인출 요청을 받은 적이 있나요?",
            "인출 금액의 사용 목적과 동행자 여부를 확인할 수 있나요?",
        ],
    },
]


def decision_router(case):
    if case["rule_score"] >= 70 or case["ml_fraud_score"] >= 0.85:
        return "Danger"
    if case["rule_score"] >= 35 or case["ml_fraud_score"] >= 0.55:
        return "Review"
    return "Clean"


def money(value, currency="KRW"):
    return f"{int(value):,} {currency}"


def decision_class(decision):
    return {
        "Danger": "danger",
        "Review": "review",
        "Clean": "clean",
    }[decision]


def decision_label(decision):
    return {
        "Danger": "위험 근거 요약 및 조사 우선순위 표시",
        "Review": "유사 사례·참고 근거 검색 후 비교 검토",
        "Clean": "정상 가능 사유 표시 및 일반 모니터링",
    }[decision]


def case_dataframe(case):
    rows = [
        ("거래 ID", case["transaction_id"]),
        ("고객 ID", case["customer_id"]),
        ("고객 맥락", case["customer_segment"]),
        ("거래 시각", case["transaction_time"]),
        ("거래 금액", money(case["amount"], case["currency"])),
        ("국가 / 채널", f"{case['country']} / {case['channel']}"),
        ("가맹점 / 업종", f"{case['merchant']} / {case['merchant_category']}"),
        ("가맹점 위험도", case["merchant_risk"]),
        ("기기 상태", case["device_status"]),
        ("계정 사용 기간", f"{case['account_age_days']}일"),
        ("최근 30일 거래 수", f"{case['past_30d_tx_count']}건"),
        ("최근 30일 평균 금액", money(case["avg_30d_amount"], case["currency"])),
    ]
    return pd.DataFrame(rows, columns=["항목", "내용"])


def build_report(case, decision):
    risk_lines = "\n".join(f"- {item}" for item in case["risk_evidence"])
    normal_lines = "\n".join(f"- {item}" for item in case["normal_evidence"])
    rule_lines = "\n".join(f"- {item}" for item in case["triggered_rules"])
    question_lines = "\n".join(f"- {item}" for item in case["customer_questions"])

    evidence_block = "Review 거래가 아니므로 유사 사례 검색은 수행하지 않았습니다."
    if decision == "Review":
        evidence_block = "\n".join(f"- {item}" for item in case["similar_cases"])

    return f"""[FraudInvestigator Lite 조사 리포트 초안]

1. 거래 요약
- 거래 ID: {case['transaction_id']}
- 고객 ID: {case['customer_id']} ({case['customer_segment']})
- 거래 금액: {money(case['amount'], case['currency'])}
- 국가/채널/업종: {case['country']} / {case['channel']} / {case['merchant_category']}
- 가맹점 위험도: {case['merchant_risk']}

2. Rule/ML 탐지 이후 분류
- Rule score: {case['rule_score']} / 100
- ML fraud score: {case['ml_fraud_score']:.2f}
- Decision Router 결과: {decision}
- 조사 의미: {decision_label(decision)}

3. Triggered Rules
{rule_lines}

4. 위험 가능 근거
{risk_lines}

5. 정상 가능 근거
{normal_lines}

6. 유사 사례·참고 근거
{evidence_block}

7. 고객 확인 질문 초안
{question_lines}

8. 조사자 확인
- 본 초안은 조사 업무 지원용이며 최종 판단은 조사자가 수행합니다.
- 본 MVP는 샘플 데이터 기반 시연 앱이며 실제 내부 FDS/API/DB와 연동되지 않습니다.
- 자동 차단 또는 자동 승인 기능을 제공하지 않습니다."""


def case_badge(decision):
    return {
        "Danger": "위험",
        "Review": "검토",
        "Clean": "정상 가능",
    }[decision]


st.markdown(
    """
    <style>
    .main .block-container {
        max-width: 1240px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stSidebar"] {
        background: #101827;
    }
    [data-testid="stSidebar"] * {
        color: #f8fafc;
    }
    .hero {
        border-radius: 8px;
        padding: 26px 28px;
        color: white;
        background:
            linear-gradient(135deg, rgba(10, 24, 46, .94), rgba(9, 86, 96, .92)),
            linear-gradient(90deg, #0f172a, #155e75);
        border: 1px solid rgba(255,255,255,.14);
        margin-bottom: 16px;
    }
    .eyebrow {
        display: inline-block;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0;
        padding: 5px 10px;
        border-radius: 999px;
        border: 1px solid rgba(255,255,255,.30);
        background: rgba(255,255,255,.12);
        margin-bottom: 12px;
    }
    .hero h1 {
        margin: 0 0 8px 0;
        font-size: 34px;
        line-height: 1.15;
        letter-spacing: 0;
    }
    .hero p {
        margin: 0;
        max-width: 900px;
        color: #dbeafe;
        font-size: 15px;
    }
    .notice {
        border-left: 4px solid #2563eb;
        background: #eff6ff;
        color: #1e3a8a;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 14px;
        margin-bottom: 18px;
    }
    .panel {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        background: white;
        padding: 18px;
        min-height: 100%;
    }
    .panel-title {
        font-size: 16px;
        font-weight: 800;
        color: #111827;
        margin-bottom: 8px;
    }
    .muted {
        color: #6b7280;
        font-size: 13px;
    }
    .decision {
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        font-size: 28px;
        font-weight: 900;
        line-height: 1.1;
        border: 1px solid;
    }
    .decision span {
        display: block;
        margin-top: 7px;
        font-size: 13px;
        font-weight: 700;
    }
    .danger {
        color: #991b1b;
        background: #fee2e2;
        border-color: #fecaca;
    }
    .review {
        color: #92400e;
        background: #fef3c7;
        border-color: #fde68a;
    }
    .clean {
        color: #065f46;
        background: #d1fae5;
        border-color: #a7f3d0;
    }
    .step {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 10px 12px;
        background: #f9fafb;
        font-size: 13px;
        min-height: 72px;
    }
    .step strong {
        display: block;
        color: #111827;
        margin-bottom: 3px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


case_options = [case["case_title"] for case in DEMO_CASES]

with st.sidebar:
    st.markdown("### 시연 케이스 큐")
    st.caption("기능명세서의 Danger / Review / Clean 흐름을 보여주기 위한 샘플입니다.")
    selected_title = st.radio("케이스 선택", case_options, label_visibility="collapsed")

    st.divider()
    st.markdown("### 시연 순서 추천")
    for idx, case in enumerate(DEMO_CASES, start=1):
        decision = decision_router(case)
        st.caption(f"{idx}. {case_badge(decision)} · {case['case_title'].replace('Case 0' + str(idx) + '. ', '')}")

    st.divider()
    st.markdown("### MVP 원칙")
    st.caption("내부 FDS/API/DB와 연동하지 않는 예선 시연")
    st.caption("Rule/ML 이후 조사 업무 지원")
    st.caption("최종 판단은 조사자가 수행")
    st.caption("자동 차단/자동 승인 없음")


case = next(item for item in DEMO_CASES if item["case_title"] == selected_title)
decision = decision_router(case)

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">JB금융그룹 Fin:AI Challenge · FraudOps MVP</div>
        <h1>FraudInvestigator Lite</h1>
        <p>기존 FDS 또는 Rule/ML 기반 1차 탐지 이후, 조사자가 의심거래의 맥락과 근거를 빠르게 확인하고 리포트 초안을 검토하도록 돕는 이상거래 조사 지원 Agent MVP입니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="notice">
    본 화면은 예선 제출용 샘플 데이터 기반 시연입니다. 실제 JB금융그룹 내부 FDS, API, DB, 규정 문서와 연동되지 않으며 AI가 최종 판단을 수행하지 않습니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.subheader(case["case_title"])
st.caption(case["demo_point"])

metric_cols = st.columns([1.05, 1, 1, 1.05])
metric_cols[0].metric("거래 금액", money(case["amount"], case["currency"]))
metric_cols[1].metric("Rule score", f"{case['rule_score']} / 100")
metric_cols[2].metric("ML fraud score", f"{case['ml_fraud_score']:.2f}")
metric_cols[3].markdown(
    f"""
    <div class="decision {decision_class(decision)}">
        {decision}
        <span>{decision_label(decision)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

steps = st.columns(6)
step_texts = [
    ("1. Input", "거래 정보 선택"),
    ("2. Context", "고객·가맹점 맥락 결합"),
    ("3. Score", "Rule/ML 점수 확인"),
    ("4. Router", "Danger/Review/Clean 분류"),
    ("5. Evidence", "Review 근거 검색"),
    ("6. Report", "리포트 초안 생성"),
]
for col, (title, body) in zip(steps, step_texts):
    col.markdown(f'<div class="step"><strong>{title}</strong>{body}</div>', unsafe_allow_html=True)

st.write("")

left, right = st.columns([1.05, 1])

with left:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">거래·고객·가맹점 맥락</div>', unsafe_allow_html=True)
    st.dataframe(case_dataframe(case), hide_index=True, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Rule/ML 판단 근거</div>', unsafe_allow_html=True)
    st.caption("Rule score")
    st.progress(case["rule_score"] / 100)
    st.caption("ML fraud score")
    st.progress(case["ml_fraud_score"])

    st.write("**Triggered Rules**")
    for rule in case["triggered_rules"]:
        st.write(f"- {rule}")

    if decision == "Danger":
        st.error("우선 검토 대상입니다. 단, 자동 차단은 수행하지 않습니다.")
    elif decision == "Review":
        st.warning("위험 가능성과 정상 가능성을 근거 기반으로 비교할 대상입니다.")
    else:
        st.success("정상 가능성이 높아 조사 우선순위를 낮출 수 있는 샘플입니다.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

evidence_col, report_col = st.columns([1, 1.15])

with evidence_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Evidence Retriever 결과</div>', unsafe_allow_html=True)
    if decision == "Review":
        evidence_rows = []
        for item in case["risk_evidence"]:
            evidence_rows.append({"구분": "위험 가능 근거", "내용": item})
        for item in case["normal_evidence"]:
            evidence_rows.append({"구분": "정상 가능 근거", "내용": item})
        for item in case["similar_cases"]:
            evidence_rows.append({"구분": "유사 사례", "내용": item})
        st.dataframe(pd.DataFrame(evidence_rows), hide_index=True, use_container_width=True)
    else:
        st.info("기능명세서 기준으로 Review 거래에 한해 유사 사례·참고 근거 검색을 수행합니다.")
        st.write("**표시 근거**")
        for item in case["risk_evidence"] + case["normal_evidence"]:
            st.write(f"- {item}")

    st.write("**고객 확인 질문 초안**")
    for question in case["customer_questions"]:
        st.write(f"- {question}")
    st.markdown("</div>", unsafe_allow_html=True)

with report_col:
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    st.markdown('<div class="panel-title">Report Generator / LLM 초안</div>', unsafe_allow_html=True)
    st.text_area(
        "조사 리포트 초안",
        build_report(case, decision),
        height=460,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "FraudInvestigator Lite는 예선 MVP 시연용 프로토타입입니다. 조사자가 근거와 리포트 초안을 검토한 뒤 최종 판단을 확정합니다."
)
