from pathlib import Path

import pandas as pd
import streamlit as st

try:
    from decision_router import route_decision
    from evidence_retriever import find_similar_evidence
    from ml_scorer import get_ml_score
    from report_generator import generate_report
    from rule_engine import calculate_rule_score
except ModuleNotFoundError:
    from src.decision_router import route_decision
    from src.evidence_retriever import find_similar_evidence
    from src.ml_scorer import get_ml_score
    from src.report_generator import generate_report
    from src.rule_engine import calculate_rule_score


st.set_page_config(
    page_title="FraudInvestigator Lite",
    page_icon="FI",
    layout="wide",
    initial_sidebar_state="expanded",
)


st.markdown(
    """
    <style>
    .main .block-container {
        padding-top: 2.2rem;
        padding-bottom: 2rem;
        max-width: 1220px;
    }
    [data-testid="stSidebar"] {
        background: #111827;
    }
    [data-testid="stSidebar"] * {
        color: #f9fafb;
    }
    .hero {
        border: 1px solid #d8dee9;
        border-radius: 8px;
        padding: 24px 26px;
        background: linear-gradient(135deg, #0f172a 0%, #17324d 52%, #105b65 100%);
        color: white;
        margin-bottom: 18px;
    }
    .hero h1 {
        font-size: 34px;
        line-height: 1.15;
        margin: 0 0 8px 0;
        letter-spacing: 0;
    }
    .hero p {
        margin: 0;
        color: #dbeafe;
        font-size: 15px;
    }
    .pill {
        display: inline-block;
        padding: 5px 10px;
        border-radius: 999px;
        background: rgba(255,255,255,.12);
        border: 1px solid rgba(255,255,255,.25);
        color: #f8fafc;
        font-size: 12px;
        margin-bottom: 12px;
    }
    .section-card {
        border: 1px solid #e5e7eb;
        border-radius: 8px;
        padding: 18px;
        background: #ffffff;
        min-height: 100%;
    }
    .section-title {
        font-size: 16px;
        font-weight: 700;
        color: #111827;
        margin-bottom: 10px;
    }
    .small-muted {
        color: #6b7280;
        font-size: 13px;
    }
    .decision-danger {
        color: #991b1b;
        background: #fee2e2;
        border: 1px solid #fecaca;
    }
    .decision-review {
        color: #92400e;
        background: #fef3c7;
        border: 1px solid #fde68a;
    }
    .decision-clean {
        color: #065f46;
        background: #d1fae5;
        border: 1px solid #a7f3d0;
    }
    .decision-box {
        border-radius: 8px;
        padding: 14px 16px;
        font-size: 22px;
        font-weight: 800;
        text-align: center;
    }
    .warning-note {
        border-left: 4px solid #2563eb;
        background: #eff6ff;
        color: #1e3a8a;
        padding: 12px 14px;
        border-radius: 6px;
        font-size: 14px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def resolve_csv_path(folder_path, flat_path):
    folder_candidate = Path(folder_path)
    flat_candidate = Path(flat_path)
    if folder_candidate.exists():
        return folder_candidate
    return flat_candidate


@st.cache_data
def load_transactions():
    return pd.read_csv(resolve_csv_path("data/sample_transactions.csv", "sample_transactions.csv"))


@st.cache_data
def load_evidence():
    return pd.read_csv(resolve_csv_path("data/evidence_samples.csv", "evidence_samples.csv"))


def format_money(value, currency):
    return f"{int(value):,} {currency}"


def decision_class(decision):
    return {
        "Danger": "decision-danger",
        "Review": "decision-review",
        "Clean": "decision-clean",
    }.get(decision, "decision-review")


def decision_message(decision):
    return {
        "Danger": "우선 검토 대상",
        "Review": "근거 확인 필요",
        "Clean": "일반 모니터링",
    }.get(decision, "검토 필요")


transactions = load_transactions()
evidence_samples = load_evidence()

with st.sidebar:
    st.markdown("### FraudInvestigator Lite")
    st.caption("Fin:AI Challenge 예선 MVP")
    st.divider()

    selected_id = st.selectbox(
        "조사 큐",
        transactions["transaction_id"].tolist(),
        format_func=lambda tx_id: (
            f"{tx_id} | "
            f"{transactions.loc[transactions['transaction_id'] == tx_id, 'customer_id'].iloc[0]} | "
            f"{int(transactions.loc[transactions['transaction_id'] == tx_id, 'amount'].iloc[0]):,} KRW"
        ),
    )

    st.divider()
    st.markdown("**MVP 원칙**")
    st.caption("실제 내부 FDS/API/DB와 연동하지 않습니다.")
    st.caption("최종 판단은 조사자가 수행합니다.")
    st.caption("자동 차단/자동 승인 기능은 제공하지 않습니다.")


transaction = transactions.loc[transactions["transaction_id"] == selected_id].iloc[0].to_dict()
rule_result = calculate_rule_score(transaction)
ml_score = get_ml_score(transaction)
decision = route_decision(rule_result["score"], ml_score)

if decision == "Review":
    evidence = find_similar_evidence(transaction, evidence_samples)
else:
    evidence = pd.DataFrame()

st.markdown(
    """
    <div class="hero">
        <div class="pill">Rule/ML 탐지 이후 조사 지원 Agent MVP</div>
        <h1>FraudInvestigator Lite</h1>
        <p>이상거래 탐지 결과를 조사자가 빠르게 해석할 수 있도록 거래 신호, 유사 근거, 리포트 초안을 한 화면에 정리합니다.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="warning-note">
    본 앱은 JB금융그룹 Fin:AI Challenge 예선용 샘플 데이터 기반 시연입니다.
    실제 내부 시스템과 연동되지 않으며, 조사자의 최종 판단을 보조하는 화면입니다.
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

summary_cols = st.columns([1.15, 1.15, 1.15, 1])
summary_cols[0].metric("거래 금액", format_money(transaction["amount"], transaction["currency"]))
summary_cols[1].metric("Rule score", f"{rule_result['score']} / 100")
summary_cols[2].metric("ML fraud score", f"{ml_score:.2f}")
summary_cols[3].markdown(
    f"""
    <div class="decision-box {decision_class(decision)}">
        {decision}<br>
        <span style="font-size:13px;font-weight:600;">{decision_message(decision)}</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")

profile_col, signal_col = st.columns([1.1, 1])

with profile_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">거래 프로파일</div>', unsafe_allow_html=True)

    profile_rows = [
        ("거래 ID", transaction["transaction_id"]),
        ("고객 ID", transaction["customer_id"]),
        ("거래 시각", transaction["transaction_time"]),
        ("국가", transaction["country"]),
        ("채널", transaction["channel"]),
        ("업종", transaction["merchant_category"]),
        ("계정 사용 기간", f"{int(transaction['account_age_days'])}일"),
        ("최근 30일 거래 수", f"{int(transaction['past_30d_tx_count'])}건"),
        ("최근 30일 평균 금액", format_money(transaction["avg_30d_amount"], transaction["currency"])),
    ]
    st.dataframe(
        pd.DataFrame(profile_rows, columns=["항목", "값"]),
        hide_index=True,
        use_container_width=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

with signal_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">조사 신호 요약</div>', unsafe_allow_html=True)

    st.caption("Rule score")
    st.progress(rule_result["score"] / 100)
    st.caption("ML fraud score")
    st.progress(ml_score)

    st.write("**Rule 근거**")
    for reason in rule_result["reasons"]:
        st.write(f"- {reason}")

    if decision == "Danger":
        st.error("우선 검토가 필요한 거래입니다. 단, 본 MVP는 자동 조치를 수행하지 않습니다.")
    elif decision == "Review":
        st.warning("유사 사례 근거를 확인하고 조사자가 판단할 거래입니다.")
    else:
        st.success("주요 이상 신호가 낮은 샘플 거래입니다.")
    st.markdown("</div>", unsafe_allow_html=True)

st.write("")

evidence_col, report_col = st.columns([1, 1.15])

with evidence_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">유사 사례 및 근거</div>', unsafe_allow_html=True)
    if decision == "Review":
        st.dataframe(
            evidence[["case_id", "case_type", "signal", "investigation_note"]],
            hide_index=True,
            use_container_width=True,
        )
    else:
        st.info("Review 분류 거래에 대해서만 근거 샘플 검색을 수행합니다.")
    st.markdown("</div>", unsafe_allow_html=True)

with report_col:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.markdown('<div class="section-title">조사 리포트 초안</div>', unsafe_allow_html=True)
    st.text_area(
        "조사자가 검토할 초안",
        generate_report(transaction, rule_result, ml_score, decision, evidence),
        height=360,
        label_visibility="collapsed",
    )
    st.markdown("</div>", unsafe_allow_html=True)

st.caption(
    "주의: FraudInvestigator Lite는 조사 업무 지원용 MVP이며, 최종 판단이나 업무 조치를 자동화하지 않습니다."
)
