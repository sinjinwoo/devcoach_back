# 🧠 RAG & LLM 기반 자기소개서 첨삭 챗봇 (AI 계절학기 프로젝트)

> 사용자 자기소개서와 채용공고를 동시에 분석하여, 인재상과의 적합도를 피드백하는 AI 기반 첨삭 서비스

---

## 📌 프로젝트 개요

- **주제**: RAG(Retrieval-Augmented Generation)과 LLM 기반의 자기소개서 첨삭 챗봇 구현
- **목표**: 변화하는 채용 요건에 따라, 사용자 자소서를 분석하고 최신 채용공고 기준에 맞춘 피드백을 제공
- **역할**: 백엔드 개발 및 시스템 설계 전반 담당 (FastAPI 기반 API 서버 개발, LLM 통신 로직 구현)

---

## 🎯 학습 목표 및 달성 방법

### 🙋🏻‍♂️ 개인 학습 목표

| 목표 | 수행 내용 |
|------|-----------|
| RAG 구조 이해 및 실제 구축 | RAG의 구성요소(Retriever, Generator 등) 학습 → 실시간성이 중요한 이번 프로젝트 특성을 반영하여 OpenAI Assistant API 기반 구조로 변형 구현 |
| FastAPI 학습 및 적용 | Django 경험은 있었지만, FastAPI는 처음 → 공식 문서 및 예제를 참고하며 경량 백엔드 서버 구축 실습<br>→ Pydantic 기반 데이터 모델 정의, JSON 직렬화, CORS 설정 등 전반 적용 |
| LLM 응답 처리 및 프론트 통신 | LLM 응답을 사용자 입력/채용공고와 함께 가공하여 prompt 구성 → 응답 결과를 JSON 형태로 반환하여 프론트와 통신 완료 |

### 👥 공동 학습 목표

- **목표**: RAG 구조를 활용해 Hallucination 및 Knowledge Cutoff 문제를 해결하는 실제 서비스 설계
- **문제정의**:
  - 다양한 회사들이 요구하는 역량과 조건은 **자주 업데이트**되며,
  - 정적 GPT만 사용 시 **정보 누락이나 환각** 가능성이 존재
- **해결 방식**:
  - 사용자가 업로드한 자소서 + 크롤링한 최신 채용공고를 함께 prompt에 포함
  - Assistant API의 `retrieval` 기능 대신 **프로그래밍적으로 문서 가공하여 동적 context 삽입**

---

## 🔧 내가 한 일과 프로젝트 기여

### ✅ 주요 구현 내용

| 구분 | 구현 내용 |
|------|-----------|
| 백엔드 서버 구축 | FastAPI 기반 REST API 서버 구축 → 사용자 입력 수신 및 응답 반환 |
| 시스템 설계 | 전체 파이프라인 흐름 설계 (사용자 입력 → 채용공고 분석 → LLM 응답) |
| API 명세서 작성 | 백엔드 ↔ 프론트 API 명세 문서화 및 공유 (GET/POST 구조, 입력/응답 형식 등) |
| LLM Prompt 구성 | 채용공고 정보와 자소서를 결합하여 시스템 메시지/사용자 메시지 구성 |
| LLM 응답 파싱 | 응답에서 첨삭 문장, 점수화, 키워드, 보완점 등 항목별로 분리하여 구조화된 JSON 반환 |
| 디버깅 및 테스트 | CORS 설정, LLM 오류 파악, 프론트 요청 오류 해결을 위해 다수의 print-debug 및 테스트 진행 |

### 📘 기술 스택

- **LLM**: OpenAI Assistant API (GPT-4 기반)
- **백엔드**: Python, FastAPI, Pydantic
- **기타**: Git, VSCode, Postman, Markdown, Notion

---

## 💡 결과 및 깨달음

### 📍 나의 행동이 만든 결과

- **시스템 흐름 및 구조 설계**를 선도하여, 팀원들이 전체 동작 맥락을 빠르게 파악할 수 있도록 기여
- LLM prompt의 역할과 응답 구조를 명확하게 정의하여 **프론트와의 원활한 통신** 달성
- API 문서와 시퀀스 다이어그램 공유로 개발 일정 관리와 병렬 작업을 가능하게 함

### ✨ 깨달음

- "코딩은 설계의 결과물이다"라는 것을 실감  
- 잘된 설계 문서는 곧 **협업의 언어**이고, 개발 일정의 핵심이라는 점을 깊이 인식하게 됨  
- 기술보다 중요한 것은 팀 간의 **소통을 위한 설계 명확화**임을 체험

---

## 🔄 새롭게 시도한 변화

| 시도 | 효과 |
|------|------|
| FastAPI 도입 | Django보다 가볍고 빠른 API 서버 구현이 가능했고, 생산성 향상 경험 |
| GPT에 의존하지 않고 디버깅 | print문, 예외 처리 등을 통해 코드 흐름을 분석하고 논리적으로 문제 추적하는 능력 향상 |
| 함수 통합 구조 설계 | 다른 백엔드 개발자의 함수들을 app.py에서 호출 가능하게 통합하여 응집력 있는 서버 구현 |
| 프론트와 명세 통일 | 변수명 컨벤션, 응답 포맷, CORS 등 조율을 통해 클라이언트 통신 매끄럽게 수행 |

---

## ⚠️ 한계 및 다음 도전

### 😥 한계

- 실시간성과 Prompt 직접제어가 중요한 서비스 특성상 **Vector DB를 활용한 Retrieval**은 사용하지 않음
- 결과적으로 LangChain 등의 RAG 파이프라인을 **직접 구현하지 못한 점은 아쉬움**

### 🚀 다음 목표

- 관심 도메인인 **금융** 분야와 AI를 접목시킨 실용 챗봇(RAG 기반) 구현
- **Vector Store + Embedding + Retriever + Generator** 전 과정 직접 구성하여 의미 있는 챗봇 고도화
- 예: 예금·적금, 대출 상품 안내 챗봇, 금융 용어 설명 챗봇 등 금융 특화 AI 서비스 기획 예정

---

## 📂 디렉토리 구조 예시

```bash
📦backend/
 ┣ 📜app.py               # FastAPI 메인 실행 파일
 ┣ 📜prompt_generator.py  # 채용공고 및 자소서를 기반으로 프롬프트 생성
 ┣ 📜openai_service.py    # Assistant API 통신 로직
 ┣ 📜schemas.py           # Pydantic 모델 정의
 ┣ 📜requirements.txt     # 패키지 의존성
