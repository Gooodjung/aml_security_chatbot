"""
AML 금융보안 챗봇 - LangGraph 기반 멀티에이전트
Conditional Edge 5개 이상 구현
"""

import os
import json
from typing_extensions import TypedDict
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import JsonOutputParser, StrOutputParser
from langgraph.graph import StateGraph, END
from dotenv import load_dotenv

load_dotenv()

# ═══════════════════════════════════════════════════════════════
# 1. STATE 정의
# ═══════════════════════════════════════════════════════════════

class ChatbotState(TypedDict):
    """챗봇 시스템 상태"""
    user_query: str                    # 사용자 질문
    transaction: dict                  # 거래 정보 (선택사항)
    routing_decision: str              # 라우팅 결정
    analysis_results: dict             # 분석 결과
    response: str                      # 최종 응답
    conversation_history: list         # 대화 이력


# ═══════════════════════════════════════════════════════════════
# 2. LLM 설정
# ═══════════════════════════════════════════════════════════════

api_key = os.getenv("OPENAI_API_KEY")
llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0.7)
analyzer_llm = ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=0)


# ═══════════════════════════════════════════════════════════════
# 3. CONDITIONAL EDGE 라우팅 함수 (5개)
# ═══════════════════════════════════════════════════════════════

def route_by_transaction_type(state: ChatbotState):
    """
    [Conditional Edge 1] 거래 유형별 분기
    wire_transfer, crypto, investment, normal 등으로 분류
    """
    if not state.get("transaction"):
        return "general_chat"

    tx_type = state["transaction"].get("type", "").lower()

    if "wire" in tx_type or "transfer" in tx_type:
        return "wire_transfer_analysis"
    elif "crypto" in tx_type:
        return "crypto_analysis"
    elif "investment" in tx_type:
        return "investment_analysis"
    else:
        return "general_transaction"


def route_by_amount(state: ChatbotState):
    """
    [Conditional Edge 2] 거래액 기반 분기
    고액(>200k) vs 저액(<=200k) 분류
    """
    if not state.get("transaction"):
        return "general_chat"

    amount = state["transaction"].get("amount", 0)
    if amount > 200000:
        return "high_amount_scrutiny"
    else:
        return "normal_amount"


def route_by_frequency(state: ChatbotState):
    """
    [Conditional Edge 3] 거래 빈도 기반 분기
    빈번(>10) vs 정상(<=10) 분류
    """
    if not state.get("transaction"):
        return "general_chat"

    frequency = state["transaction"].get("frequency", 0)
    if frequency > 10:
        return "frequent_transaction_alert"
    else:
        return "normal_frequency"


def route_by_risk_country(state: ChatbotState):
    """
    [Conditional Edge 4] 위험 국가 기반 분기
    고위험 국가(RU, KP, IR 등) 감지
    """
    if not state.get("transaction"):
        return "general_chat"

    high_risk_countries = ["RU", "KP", "IR", "SY", "CU"]
    source = state["transaction"].get("source_country", "")
    dest = state["transaction"].get("dest_country", "")

    if source in high_risk_countries or dest in high_risk_countries:
        return "high_risk_country_alert"
    else:
        return "normal_country"


def route_by_channel(state: ChatbotState):
    """
    [Conditional Edge 5] 채널 기반 분기
    온라인, 오프라인, 암호화폐 채널별 분류
    """
    if not state.get("transaction"):
        return "general_chat"

    channel = state["transaction"].get("channel", "").lower()

    if "crypto" in channel:
        return "crypto_channel_handling"
    elif "online" in channel:
        return "online_channel_handling"
    else:
        return "offline_channel_handling"


# ═══════════════════════════════════════════════════════════════
# 4. NODE 함수들
# ═══════════════════════════════════════════════════════════════

def init_chat(state: ChatbotState):
    """초기화: 사용자 입력 처리"""
    return {
        "routing_decision": "initialized",
        "conversation_history": [
            {"role": "user", "content": state["user_query"]}
        ]
    }


def general_chat(state: ChatbotState):
    """일반 질문에 대한 답변"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 친절한 금융보안 상담사입니다. 사용자의 질문에 도움이 되는 답변을 제공하세요."),
        ("human", "{query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"query": state["user_query"]})

    return {"response": response}


def wire_transfer_analysis(state: ChatbotState):
    """전신송금 거래 분석"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 AML 전문가입니다. 전신송금 거래의 위험도를 분석하세요."),
        ("human", "거래: {transaction}\n질문: {query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"type": "wire_transfer"}}


def crypto_analysis(state: ChatbotState):
    """암호화폐 거래 분석"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 암호화폐 자금세탁 탐지 전문가입니다. 암호화폐 거래의 위험성을 평가하세요."),
        ("human", "거래: {transaction}\n질문: {query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"type": "crypto"}}


def investment_analysis(state: ChatbotState):
    """투자 거래 분석"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 투자 자금세탁 탐지 전문가입니다. 투자 거래의 의심도를 평가하세요."),
        ("human", "거래: {transaction}\n질문: {query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"type": "investment"}}


def high_amount_scrutiny(state: ChatbotState):
    """고액 거래 집중 검토"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 고액거래 감시 전문가입니다. 고액 거래는 자금세탁 위험이 높습니다."),
        ("human", "고액거래 정보: {transaction}\n질문: {query}\n\n고액 거래에 대한 집중 검토 의견을 제시하세요.")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"alert": "high_amount"}}


def frequent_transaction_alert(state: ChatbotState):
    """빈번 거래 경고"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 거래 패턴 분석 전문가입니다. 빈번한 거래는 Layering 자금세탁의 신호입니다."),
        ("human", "빈번 거래 정보: {transaction}\n질문: {query}\n\n이 거래 패턴의 위험성을 평가하세요.")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"alert": "frequent_transaction"}}


def high_risk_country_alert(state: ChatbotState):
    """고위험 국가 경고"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 국제거래 규제 전문가입니다. 고위험 국가와의 거래는 FATF 제재 대상입니다."),
        ("human", "국제거래 정보: {transaction}\n질문: {query}\n\n규제 위험성을 평가하세요.")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"alert": "high_risk_country"}}


def crypto_channel_handling(state: ChatbotState):
    """암호화폐 채널 처리"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 암호화폐 채널 감시 전문가입니다."),
        ("human", "암호화폐 채널 거래: {transaction}\n질문: {query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response, "analysis_results": {"channel": "crypto"}}


def general_transaction(state: ChatbotState):
    """일반 거래 처리"""
    prompt = ChatPromptTemplate.from_messages([
        ("system", "당신은 거래 분석가입니다."),
        ("human", "거래: {transaction}\n질문: {query}")
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({
        "transaction": json.dumps(state["transaction"]),
        "query": state["user_query"]
    })

    return {"response": response}


# ═══════════════════════════════════════════════════════════════
# 5. 그래프 구성
# ═══════════════════════════════════════════════════════════════

def build_chatbot_graph():
    """챗봇 그래프 구축"""
    workflow = StateGraph(ChatbotState)

    # 노드 추가
    workflow.add_node("init", init_chat)
    workflow.add_node("general_chat", general_chat)
    workflow.add_node("wire_transfer_analysis", wire_transfer_analysis)
    workflow.add_node("crypto_analysis", crypto_analysis)
    workflow.add_node("investment_analysis", investment_analysis)
    workflow.add_node("high_amount_scrutiny", high_amount_scrutiny)
    workflow.add_node("frequent_transaction_alert", frequent_transaction_alert)
    workflow.add_node("high_risk_country_alert", high_risk_country_alert)
    workflow.add_node("crypto_channel_handling", crypto_channel_handling)
    workflow.add_node("general_transaction", general_transaction)
    workflow.add_node("normal_amount", general_transaction)
    workflow.add_node("normal_frequency", general_transaction)
    workflow.add_node("normal_country", general_transaction)
    workflow.add_node("online_channel_handling", general_transaction)
    workflow.add_node("offline_channel_handling", general_transaction)

    # 시작점
    workflow.set_entry_point("init")

    # Conditional Edge 1: 거래 유형별 분기
    workflow.add_conditional_edges(
        "init",
        route_by_transaction_type,
        {
            "general_chat": "general_chat",
            "wire_transfer_analysis": "wire_transfer_analysis",
            "crypto_analysis": "crypto_analysis",
            "investment_analysis": "investment_analysis",
            "general_transaction": "general_transaction"
        }
    )

    # Conditional Edge 2: 거래액 기반 분기
    workflow.add_conditional_edges(
        "wire_transfer_analysis",
        route_by_amount,
        {
            "general_chat": "general_chat",
            "high_amount_scrutiny": "high_amount_scrutiny",
            "normal_amount": "normal_amount"
        }
    )

    # Conditional Edge 3: 거래 빈도 기반 분기
    workflow.add_conditional_edges(
        "crypto_analysis",
        route_by_frequency,
        {
            "general_chat": "general_chat",
            "frequent_transaction_alert": "frequent_transaction_alert",
            "normal_frequency": "normal_frequency"
        }
    )

    # Conditional Edge 4: 위험 국가 기반 분기
    workflow.add_conditional_edges(
        "investment_analysis",
        route_by_risk_country,
        {
            "general_chat": "general_chat",
            "high_risk_country_alert": "high_risk_country_alert",
            "normal_country": "normal_country"
        }
    )

    # Conditional Edge 5: 채널 기반 분기
    workflow.add_conditional_edges(
        "general_transaction",
        route_by_channel,
        {
            "general_chat": "general_chat",
            "crypto_channel_handling": "crypto_channel_handling",
            "online_channel_handling": "online_channel_handling",
            "offline_channel_handling": "offline_channel_handling"
        }
    )

    # 최종 엣지 (각 분석이 끝나면 END)
    workflow.add_edge("general_chat", END)
    workflow.add_edge("high_amount_scrutiny", END)
    workflow.add_edge("frequent_transaction_alert", END)
    workflow.add_edge("high_risk_country_alert", END)
    workflow.add_edge("crypto_channel_handling", END)
    workflow.add_edge("normal_amount", END)
    workflow.add_edge("normal_frequency", END)
    workflow.add_edge("normal_country", END)
    workflow.add_edge("online_channel_handling", END)
    workflow.add_edge("offline_channel_handling", END)

    return workflow.compile()


# ═══════════════════════════════════════════════════════════════
# 6. 챗봇 실행
# ═══════════════════════════════════════════════════════════════

def chat(user_query: str, transaction: dict = None):
    """챗봇과의 대화"""
    graph = build_chatbot_graph()

    initial_state = {
        "user_query": user_query,
        "transaction": transaction or {},
        "routing_decision": "",
        "analysis_results": {},
        "response": "",
        "conversation_history": []
    }

    result = graph.invoke(initial_state)
    return result["response"]


if __name__ == "__main__":
    # 테스트
    print("=== AML 금융보안 챗봇 ===\n")

    # 일반 질문
    response1 = chat("자금세탁(AML)이란 무엇인가요?")
    print(f"Q: 자금세탁(AML)이란 무엇인가요?\nA: {response1}\n")

    # 거래 분석
    transaction = {
        "id": "TXN-001",
        "amount": 500000,
        "type": "wire_transfer",
        "channel": "online",
        "source_country": "RU",
        "dest_country": "US",
        "frequency": 15
    }

    response2 = chat("이 거래는 안전한가요?", transaction)
    print(f"Q: 이 거래는 안전한가요?\nA: {response2}\n")
