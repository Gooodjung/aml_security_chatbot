"""
AML 금융보안 챗봇 - Streamlit 대시보드
"""

import streamlit as st
import json
from src.aml_chatbot import chat

st.set_page_config(
    page_title="AML 금융보안 챗봇",
    page_icon="🔍",
    layout="wide"
)

st.title("🔍 AML 금융보안 챗봇")
st.markdown("---")

# Sidebar: 네비게이션
with st.sidebar:
    st.header("메뉴")
    page = st.radio(
        "페이지 선택",
        ["💬 챗봇", "📊 거래 분석", "📈 벤치마크"]
    )

# ─────────────────────────────────────────────────────────────
# Page 1: 챗봇
# ─────────────────────────────────────────────────────────────

if page == "💬 챗봇":
    st.header("금융보안 상담 챗봇")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("💬 대화")
        user_input = st.text_area(
            "질문을 입력하세요",
            placeholder="예: 자금세탁의 3단계는?",
            height=100
        )

        if st.button("🚀 전송", use_container_width=True):
            with st.spinner("답변 생성 중..."):
                response = chat(user_input)
                st.session_state.last_response = response

    with col2:
        st.subheader("📋 답변")
        if "last_response" in st.session_state:
            st.info(st.session_state.last_response)
        else:
            st.info("답변이 여기에 표시됩니다.")

    st.markdown("---")
    st.subheader("자주 하는 질문")
    faqs = [
        "자금세탁(AML)이란 무엇인가요?",
        "Placement, Layering, Integration은?",
        "의심거래 보고(STR)는 어떻게 하나요?",
        "암호화폐 자금세탁의 특징은?",
    ]

    for faq in faqs:
        if st.button(f"❓ {faq}", use_container_width=True):
            with st.spinner("답변 생성 중..."):
                response = chat(faq)
                st.success(response)

# ─────────────────────────────────────────────────────────────
# Page 2: 거래 분석
# ─────────────────────────────────────────────────────────────

elif page == "📊 거래 분석":
    st.header("거래 분석")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("거래 정보 입력")

        amount = st.number_input("거래액 ($)", value=50000, min_value=0, step=1000)
        tx_type = st.selectbox(
            "거래 유형",
            ["wire_transfer", "crypto_exchange", "investment", "normal_transfer"]
        )
        channel = st.selectbox(
            "채널",
            ["online", "branch", "atm", "crypto"]
        )
        source_country = st.selectbox(
            "출발국",
            ["KR", "US", "CN", "JP", "RU", "SG", "HK"]
        )
        dest_country = st.selectbox(
            "도착국",
            ["US", "CN", "JP", "RU", "SG", "HK", "KR"]
        )
        frequency = st.slider("거래 빈도 (24h)", 0, 50, 5)

        analyze_button = st.button("🔍 분석", use_container_width=True)

    with col2:
        st.subheader("분석 결과")

        if analyze_button:
            transaction = {
                "amount": amount,
                "type": tx_type,
                "channel": channel,
                "source_country": source_country,
                "dest_country": dest_country,
                "frequency": frequency
            }

            query = f"거래액 ${amount}, {tx_type} 유형, {source_country}→{dest_country} 국제거래입니다. 위험도는?"

            with st.spinner("분석 중..."):
                response = chat(query, transaction)

            st.success("✅ 분석 완료")
            st.info(response)

            # 거래 정보 표시
            st.subheader("거래 세부정보")
            col_t1, col_t2, col_t3 = st.columns(3)
            with col_t1:
                st.metric("거래액", f"${amount:,}")
            with col_t2:
                st.metric("거래 유형", tx_type)
            with col_t3:
                st.metric("거래 빈도", f"{frequency}회/24h")

# ─────────────────────────────────────────────────────────────
# Page 3: 벤치마크
# ─────────────────────────────────────────────────────────────

elif page == "📈 벤치마크":
    st.header("평가 결과")

    st.subheader("오픈소스 벤치마크")
    benchmark_data = {
        "벤치마크": ["MMLU", "TruthfulQA", "GPQA (diamond)"],
        "점수": ["75%", "4.3/5.0", "65%"],
        "상태": ["✅ 완료", "✅ 완료", "✅ 완료"]
    }
    st.table(benchmark_data)

    st.subheader("자체 텍소노미 평가")

    col_tax1, col_tax2 = st.columns(2)

    with col_tax1:
        st.metric("Fluency (유창성)", "7/10", "자연스러운 표현")
        st.metric("Factuality (사실성)", "8/10", "정보 정확도")

    with col_tax2:
        st.metric("Bias (편향성)", "3/10", "낮을수록 좋음")
        st.metric("Coherence (일관성)", "7/10", "논리적 흐름")

    st.markdown("---")
    st.info("📌 평가는 Jupyter 노트북 [실습3]에서 상세히 진행됩니다.")

st.markdown("---")
st.caption("🤖 AML 금융보안 챗봇 | LangGraph × OpenAI")
