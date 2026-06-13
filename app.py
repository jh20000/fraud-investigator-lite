import pandas as pd
import streamlit as st

from src.decision_router import route_decision
from src.evidence_retriever import find_similar_evidence
from src.ml_scorer import get_ml_score
from src.report_generator import generate_report
from src.rule_engine import calculate_rule_score


st.set_page_config(page_title="FraudInvestigator Lite", layout="wide")


@st.cache_data
def load_transactions():
    return pd.read_csv("data/sample_transactions.csv")


@st.cache_data
def load_evidence():
    return pd.read_csv("data/evidence_samples.csv")


st.title("FraudInvestigator Lite")
st.caption("JB금융그룹 Fin:AI Challenge 예선 MVP용 샘플 데이터 기반 이상거래 조사 지원 시연 앱")

st.info(
    "본 앱은 실제 JB금융그룹 내부 FDS, API, DB와 연동되지 않은 예선 MVP입니다. "
    "Rule/ML 탐지 이후 조사 업무를 보조하기 위한 샘플 시연이며, 최종 판단은 조사자가 수행합니다."
)

transactions = load_transactions()
evidence_samples = load_evidence()

selected_id = st.selectbox(
    "조사할 샘플 거래 선택",
    transactions["transaction_id"].tolist(),
    format_func=lambda tx_id: f"{tx_id} - {transactions.loc[transactions['transaction_id'] == tx_id, 'customer_id'].iloc[0]}",
)

transaction = transactions.loc[transactions["transaction_id"] == selected_id].iloc[0].to_dict()
rule_result = calculate_rule_score(transaction)
ml_score = get_ml_score(transaction)
decision = route_decision(rule_result["score"], ml_score)

left, right = st.columns([1.15, 1])

with left:
    st.subheader("거래 정보")
    st.dataframe(pd.DataFrame([transaction]), hide_index=True, use_container_width=True)

with right:
    st.subheader("탐지 이후 조사 신호")
    metric_cols = st.columns(3)
    metric_cols[0].metric("Rule score", f"{rule_result['score']}")
    metric_cols[1].metric("ML fraud score", f"{ml_score:.2f}")
    metric_cols[2].metric("분류", decision)

    st.write("Rule 근거")
    for reason in rule_result["reasons"]:
        st.write(f"- {reason}")

st.divider()

if decision == "Review":
    st.subheader("유사 사례 및 근거 샘플")
    evidence = find_similar_evidence(transaction, evidence_samples)
    st.dataframe(evidence, hide_index=True, use_container_width=True)
else:
    evidence = pd.DataFrame()
    st.subheader("유사 사례 및 근거 샘플")
    st.write("Review 분류 거래에 대해서만 근거 샘플 검색을 수행합니다.")

st.subheader("조사 리포트 초안")
st.text_area(
    "조사자가 검토할 초안",
    generate_report(transaction, rule_result, ml_score, decision, evidence),
    height=320,
)

st.caption("주의: 이 화면은 조사자의 판단을 대체하지 않으며, 자동 차단 또는 자동 승인 기능을 제공하지 않습니다.")
