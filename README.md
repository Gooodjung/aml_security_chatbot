# 🔍 AML 금융보안 챗봇 (AML Security Chatbot)

LangChain과 LangGraph를 활용한 **금융 자금세탁방지(AML) 전문 챗봇** 시스템

## 📊 프로젝트 개요

**주제**: 나만의 AML 금융보안 챗봇
- Streamlit 배포 링크: https://amlsecuritychatbot-inuee97pwsyhto46qpwneu.streamlit.app/
- Placement, Layering, Integration 3단계 자금세탁 탐지
- LangGraph 기반 멀티에이전트 시스템
- 5개 이상의 Conditional Edge 구현
- 오픈소스 벤치마크 + 자체 텍소노미 평가

```

## 📁 프로젝트 구조

```
aml_security_chatbot/
├── notebooks/
│   ├── [실습1] LangGraph와 Conditional Edge.ipynb
│   ├── [실습2] AML 금융보안 챗봇 구현.ipynb
│   └── [실습3] 벤치마크 평가.ipynb
├── src/
│   ├── aml_chatbot.py      # 챗봇 구현 (Conditional Edge 5개)
│   └── evaluator.py        # 평가 파이프라인
├── data/
│   └── sample_transactions.csv
├── app.py                  # Streamlit 대시보드
├── requirements.txt
├── .env.example
└── README.md
```

## ✨ 주요 기능

### 1. **Conditional Edge 5개 이상**
- ✅ Router: 거래 유형 기반 분기
- ✅ 거래액 기반: High/Low 분기
- ✅ 거래 빈도 기반: Frequent/Infrequent 분기
- ✅ 지역 위험도 기반: High-risk Country 감지
- ✅ 채널 기반: Online/Offline 분기

### 2. **오픈소스 벤치마크**
- MMLU (지식 기반 평가)
- TruthfulQA (사실성 평가)
- GPQA (고난도 질문 답변)

### 3. **자체 텍소노미 평가**
- **Fluency** (유창성): 챗봇 답변의 자연스러움
- **Factuality** (사실성): 제공 정보의 정확도
- **Bias** (편향성): 중립성 평가
- **Coherence** (일관성): 맥락 이해도

## 실행 경로

### 1: LangGraph와 Conditional Edge
- LangGraph 기초 개념
- State와 Node 정의
- 5가지 조건부 엣지 구현
- 그래프 구조 시각화

### 2: AML 금융보안 챗봇
- 챗봇 아키텍처 설계
- AML 탐지 로직 구현
- LLM 체인 구성
- 실제 거래 분석

### 3: 벤치마크 평가
- 오픈소스 벤치마크 (MMLU, TruthfulQA, GPQA)
- 자체 텍소노미 정의 및 구현
- 평가 파이프라인 실행
- 결과 시각화 및 분석

