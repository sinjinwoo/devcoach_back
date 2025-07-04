# ✨ DeCo (DevCoach): AI 기반 자기소개서 첨삭 서비스

> "합격에 가까워지는 글쓰기, DeCo가 함께합니다."  
> 기업의 채용 공고를 분석해 당신의 자소서를 정밀하게 첨삭해드립니다.

---
## 🧩 서비스 개요
DeCo는 크롤링 → OCR 처리 → LLM 분석 → RAG 기반 피드백으로 이어지는
AI 자소서 코칭 파이프라인을 통해 사용자의 자기소개서를 기업 요구사항에 맞게 자동 분석 및 첨삭해주는 서비스입니다.

기업명 입력만 하면 사람인 등의 채용 플랫폼에서 해당 기업의 채용 공고를 크롤링

OCR을 활용해 이미지형 채용 포스터도 분석

RAG 기반 4o-mini 모델로 문항별 핵심 표현력, 직무 연관성, 문법 오류 등을 정밀 분석

---
## 🚀 배포 주소

- 서비스 주소: [DevCoach](http://13.125.251.159/) 

---

## ⚙️ 실행 방법 (로컬)

```bash
# 백엔드 실행
cd backend
python -m venv venv
source venv/bin/activate   # 윈도우: venv\Scripts\activate
pip install -r requirements.txt
python final.py

```

```bash
# 프론트 실행
cd frontend-local
npm install
npm run dev
```

---
## 📅 프로젝트 기간
2025.06.23 ~ 2025.07.04

---
## 👨‍👩‍👧‍👦 팀원 소개

|[신진우](https://github.com/sinjinwoo)|[임덕규](https://github.com/Deokguu/)|
| :------------------------------------------------------------: | :----------------------------------------------------------: |
| ![sinjinwoo](https://avatars.githubusercontent.com/sinjinwoo?v=4) | ![hy2min](https://avatars.githubusercontent.com/Deokguu?v=4) |

|[박준수](https://github.com/junsudada)|[김민학](https://github.com/Python-taker/)|
| :------------------------------------------------------------: | :----------------------------------------------------------: |
| ![junsudada](https://avatars.githubusercontent.com/junsudada?v=4) | ![Python-taker](https://avatars.githubusercontent.com/Python-taker?v=4) |

## 🛠️ 기술 스택

<br>
<img src="https://img.shields.io/badge/vue.js-4FC08D?style=flat-square&logo=vuedotjs&logoColor=white"/> 
<img src="https://img.shields.io/badge/fastapi-092E20?style=flat-square&logo=fastapi&logoColor=white"/> 
<img src="https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white"/>
<img src="https://img.shields.io/badge/tailwind-412991?style=flat-square&logo=tailwindcss&logoColor=white"/>

<br>


<img src="https://img.shields.io/badge/Amazon%20EC2-FF9900?style=flat-square&logo=amazonec2&logoColor=white"/>
<img src="https://img.shields.io/badge/Nginx-009639?style=flat-square&logo=nginx&logoColor=white"/>
<img src="https://img.shields.io/badge/Gunicorn-499848?style=flat-square&logo=gunicorn&logoColor=white"/>

## 🖥️ 서버 아키텍처 구성
    
 -  **EC2**: 클라우드 서버 호스팅  
 - **Nginx**: 정적 파일 서빙   
 - **Gunicorn**: FastApi WSGI 애플리케이션 실행

## 👨‍🔧 팀원별 역할 분담

### 🧑‍💻 신진우

- **담당 영역**: 프론트엔드 전체 페이지 구성, 서버 배포
 
- **배포**
  - AWS EC2 기반 전체 인프라 구성 (Nginx, Gunicorn)
  
---

### 🧑‍💻 박준수

### 🧑‍💻 김민학

### 🧑‍💻 임덕규

---
## 🔍 핵심 기능

### ✅ 채용공고 분석 (OCR + 크롤링)

- 사람인 플랫폼에서 채용정보 수집

- 이미지 형태의 공고는 OCR을 통해 텍스트 추출

- 필수요건, 우대사항, 직무역량 등 키워드 자동 정제

### ✅ 자기소개서 첨삭
- 문항 단위로 첨삭 진행

- 공고 분석 내용 바탕으로 사용자의 자기소개서 문항과 답변 분석

- 사용자의 답변을 적합성, 보완/개선 제안, 가산전 요소와 표현 등으로 세분화하여 피드백

---
## 📈 향후 개발 방향

- 합격 자소서 데이터셋 확보 → 피드백 품질 향상

- 유저별 개선 추이 분석 기능 도입 → 자기 발전 추적 가능하게

- 문서 업로드 통한 이력서/자소서 자동 분석 기능 추가
