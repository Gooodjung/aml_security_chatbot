# 🔍 AML 금융보안 챗봇 (AML Security Chatbot)

LangChain과 LangGraph를 활용한 **금융 자금세탁방지(AML) 전문 챗봇** 시스템

## 📊 프로젝트 개요

**주제**: 나만의 AML 금융보안 챗봇
- Placement, Layering, Integration 3단계 자금세탁 탐지
- LangGraph 기반 멀티에이전트 시스템
- 5개 이상의 Conditional Edge 구현
- 오픈소스 벤치마크 + 자체 텍소노미 평가

## 🚀 빠른 시작

```bash
# 1. 프로젝트 폴더 이동
cd ~/aml_security_chatbot

# 2. 가상환경 설정
python -m venv venv
source venv/bin/activate

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경 변수 설정
cp .env.example .env
# .env 파일에서 OPENAI_API_KEY 입력

# 5. 실습 노트북 실행
jupyter notebook notebooks/

# 또는 Streamlit 대시보드 실행
streamlit run app.py
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

## 📖 학습 경로

### 실습 1: LangGraph와 Conditional Edge
- LangGraph 기초 개념
- State와 Node 정의
- 5가지 조건부 엣지 구현
- 그래프 구조 시각화

### 실습 2: AML 금융보안 챗봇
- 챗봇 아키텍처 설계
- AML 탐지 로직 구현
- LLM 체인 구성
- 실제 거래 분석

### 실습 3: 벤치마크 평가
- 오픈소스 벤치마크 (MMLU, TruthfulQA, GPQA)
- 자체 텍소노미 정의 및 구현
- 평가 파이프라인 실행
- 결과 시각화 및 분석

## 🎯 과제 제출 형식

```
주제: 나만의 AML 금융보안 챗봇

Streamlit 배포 링크: (배포 후 추가)

선택 옵션 리스트:
✓ LangGraph의 Conditional Edge 5개 구현
✓ 오픈소스 벤치마크 평가
  - MMLU: XX%
  - TruthfulQA: X.X / 5
  - GPQA (diamond): XX%

텍소노미 별 평가:
✓ Fluency: X/10
✓ Factuality: X/10
✓ Bias: X/10
✓ Coherence: X/10
```

## 📞 문제 해결

### API 오류
```bash
# .env 확인
cat .env

# 또는 환경 변수 확인
echo $OPENAI_API_KEY
```

### Jupyter 실행 오류
```bash
# 커널 재설치
python -m ipykernel install --user --name venv --display-name "Python (venv)"
```

---

완성되었습니다! 🎉
