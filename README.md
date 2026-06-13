# FraudInvestigator Lite

JB금융그룹 Fin:AI Challenge 예선 MVP용 Streamlit 시연 앱입니다.

FraudInvestigator Lite는 기존 FDS를 대체하는 서비스가 아니라, Rule/ML 탐지 이후 이상거래 조사 업무를 지원하는 AI Agent 콘셉트의 최소 시연 앱입니다. 본 레포는 제안서와 기능명세서 흐름이 실제로 돌아가는 샘플 데이터 기반 MVP를 목표로 합니다.

## 주의사항

- 실제 JB금융그룹 내부 FDS, API, DB와 연동되지 않습니다.
- LLM이 최종 판단을 수행하지 않습니다.
- 자동 차단 또는 자동 승인 기능을 제공하지 않습니다.
- 최종 판단은 조사자가 수행합니다.
- 예선 MVP 제출을 위한 샘플 데이터 기반 시연 앱입니다.

## 주요 흐름

1. 샘플 거래 선택
2. 거래 정보 표시
3. Rule score 및 ML fraud score 표시
4. Danger / Review / Clean 분류
5. Review 거래에 대해서만 유사 사례 및 근거 샘플 검색
6. 조사자가 검토할 리포트 초안 생성

## 프로젝트 구조

```text
.
├── app.py
├── data/
│   ├── sample_transactions.csv
│   └── evidence_samples.csv
├── src/
│   ├── decision_router.py
│   ├── evidence_retriever.py
│   ├── ml_scorer.py
│   ├── report_generator.py
│   └── rule_engine.py
├── requirements.txt
└── README.md
```

## 실행 방법

```bash
pip install -r requirements.txt
streamlit run app.py
```

## 분류 기준

- `Danger`: Rule score가 높거나 ML fraud score가 높은 거래
- `Review`: 조사자 검토가 필요한 중간 위험 거래
- `Clean`: 주요 이상 신호가 낮은 거래

이 분류는 조사 우선순위 지원용이며, 최종 판단이나 업무 조치를 자동화하지 않습니다.
