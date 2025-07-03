# pip install fastapi uvicorn openai python-dotenv
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from crawling import fetch_recruitment_info,convert_to_recruitment_info
from fastapi import Query

app = FastAPI()

# Allow CORS for local dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, restrict this to your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/search")
async def search_endpoint(company: str = Query(...)):
    print(f"Received company: {company}")
    data = fetch_recruitment_info(company)
    ans = convert_to_recruitment_info(data)

    if not ans:
        return {"message": "No recruitment information found."}
    
    return ans

class JobDescriptionRequest(BaseModel):
    company: str
    url : str
    
@app.post("/jobdescription")
async def chat_endpoint(req: JobDescriptionRequest):
    # 회사
    company = req.company
    # url
    url = req.url

    print(f"Received company: {company}, url: {url}")

    job_list = [
  {
    "직무명": "FW개발",
    "담당업무": [
      "진단 장비 S/W 개발",
      "MCU 프로그램 개발"
    ],
    "자격요건": [
      "경력 5년 이상"
    ],
    "필수사항": [
      "None"
    ],
    "우대사항": [
      "차량 CAN/Ethernet/OTA통신 경험자",
      "다양한 통신 프로토콜 연동 처리 경험자",
      "RTOS 개발 경험자",
      "회로도 이해 가능자",
      "CI/CD 경험자",
      "Linux 개발 경험자"
    ],
    "인재상": [
      "열정과 도전",
      "소통과 협력",
      "창의와 혁신",
      "학습과 성장",
      "직무전문성",
      "고객지향성",
      "문제해결",
      "세밀한 일처리",
      "성실성",
      "프로젝트 관리",
      "시장 이해",
      "추진력"
    ]
  },
  {
    "직무명": "리눅스 개발",
    "담당업무": [
      "진단 장비 S/W 개발",
      "차량 OTA 제어기 리프로그램 모듈 개발",
      "Embedded Linux 시스템/응용 프로그램 개발"
    ],
    "자격요건": [
      "경력 5년 이상"
    ],
    "필수사항": [
      "None"
    ],
    "우대사항": [
      "차량 CAN/Ethernet/OTA통신 경험자",
      "다양한 통신 프로토콜 연동/영상자료 처리 경험자",
      "Linux 시스템 및 운영 서비스 등 관련 경험 및 이해자",
      "TCP/IP, UDP를 사용한 Network Program 경험자",
      "회로도 이해 가능자",
      "CI/CD 경험자",
      "MCU FW 개발 경험자"
    ],
    "인재상": [
      "열정과 도전",
      "소통과 협력",
      "창의와 혁신",
      "학습과 성장",
      "직무전문성",
      "고객지향성",
      "문제해결",
      "세밀한 일처리",
      "성실성",
      "프로젝트 관리",
      "시장 이해",
      "추진력"
    ]
  },
  {
    "직무명": "차량 소프트웨어개발 검증",
    "담당업무": [
      "전장/윈도우 소프트웨어 검증 및 자동화 도구(CT) 개발",
      "C++ / Python 활용한 Application 개발"
    ],
    "자격요건": [
      "컴퓨터/전산 관련 학과 학사 졸업 이상",
      "C++ 기반 소프트웨어 프로그램 개발 능력 필수",
      "Python을 활용한 개발 경험"
    ],
    "필수사항": [
      "None"
    ],
    "우대사항": [
      "SW 검증 자동화 툴 구축 경험 (CT 포함)",
      "Whitebox 테스트 관련 개발 경험 (테스트 설계 및 구현 개발 등)",
      "차량 통신 소프트웨어 개발 경험 (CAN, DoIP 등 프로토콜)",
      "CANoe 및 CAPL 스크립트 개발 경험",
      "차량 ECU 진단 및 통신 프로세스 이해",
      "소프트웨어 품질 관리를 위한 CI/CD/CT 도구 활용 경험"
    ],
    "인재상": [
      "열정과 도전",
      "소통과 협력",
      "창의와 혁신",
      "학습과 성장",
      "직무전문성",
      "고객지향성",
      "문제해결",
      "세밀한 일처리",
      "성실성",
      "프로젝트 관리",
      "시장 이해",
      "추진력"
    ]
  },
  {
    "직무명": "앱 개발",
    "담당업무": [
      "현대/기아/제네시스 공식 차량 진단 솔루션 개발 (GDS-Smart, KDS 2.0)",
      "공식 진단 서비스 개발 : 차량 상태 모니터링, 고장 진단, 특수 항목 진단 및 검사 프로그램 개발",
      "BT/BLE/네트워크 통신을 통한 Third Device 통신 및 기능 개발 : 진단통신모듈 (BT, Wi-Fi Direct, USB), 간극측정(BLE), 기밀검사(BLE) 장비 통신 및 기능 개발",
      "서버 연계 리포트기능 개발",
      "고객 인도전 신차 검사 서비스 개발 (PDI)",
      "차량 검사를 위한 진단 통신 프로그램 개발 : 차량 내 전자제어기들과의 통신을 통한 자동 검사 기능 개발",
      "현대/기아/제네시스 해외 다수 국가 운영 및 대응"
    ],
    "자격요건": [
      "경력 7년 이상",
      "IT부문 학사 이상"
    ],
    "필수사항": [
      "None"
    ],
    "우대사항": [
      "안드로이드 앱 개발 5년 이상 수행하신 분",
      "고객 요구사항에 대한 분석/검토 가능한 분",
      "SW 구조 설계, HW 외부 모듈 유/무선 연동 개발 경험자 우대",
      "MVVM, 디자인패턴 등 아키텍쳐에 대한 이해와 관심이 있는 분",
      "데이터베이스, 서버통신에 이해와 경험이 있는 분",
      "안드로이드 Automotive용 App 개발 유경험자"
    ],
    "인재상": [
      "열정과 도전",
      "소통과 협력",
      "창의와 혁신",
      "학습과 성장",
      "직무전문성",
      "고객지향성",
      "문제해결",
      "세밀한 일처리",
      "성실성",
      "프로젝트 관리",
      "시장 이해",
      "추진력"
    ]
  },
  {
    "직무명": "Back-End 개발",
    "담당업무": [
      "Spring Framework를 활용한 웹 서비스 및 API 개발",
      "Java 1.8 이상의 Stream, Lambda 등 함수형 프로그래밍 활용",
      "비즈니스 목표와 요구사항을 이해하고, 이를 소프트웨어로 구현한 경험",
      "RDBMS 기반 데이터 모델링, 쿼리 작성 및 성능 튜닝",
      "HTML, CSS3, x-x-javascript(ES6+)를 이용한 UI/UX 개발 경험",
      "원활한 커뮤니케이션 및 협업, 다양한 이해관계자와의 소통 역량"
    ],
    "자격요건": [
      "경력 3년 이상 ~ 15년 이하"
    ],
    "필수사항": [
      "None"
    ],
    "우대사항": [
      "높은 사용자 수와 데이터 트래픽을 안정적으로 처리할 수 있는 시스템을 구축하고 운영한 경험",
      "메시지 큐(Kafka, RabbitMQ 등)를 활용한 비동기 시스템 연동 및 데이터 처리 경험",
      "리눅스 서버 환경 설정, Nginx/Apache/Tomcat 등 웹 및 애플리케이션 서버 구성 운영 경험",
      "Spring WebFlux, Reactor 등 리액티브 스택을 활용한 비동기/논블로킹 데이터 처리 경험",
      "신규 서비스 기획 또는 대규모 시스템의 구조 설계, 아키텍처 수립 및 요구사항 분석 경험"
    ],
    "인재상": [
      "열정과 도전",
      "소통과 협력",
      "창의와 혁신",
      "학습과 성장",
      "직무전문성",
      "고객지향성",
      "문제해결",
      "세밀한 일처리",
      "성실성",
      "프로젝트 관리",
      "시장 이해",
      "추진력"
    ]
  }
]

    return job_list

class AssistantRequest(BaseModel):
    company: str
    position: str
    qualifications: str = ""
    requirements: str = ""
    duties: str = ""
    preferred: str = ""
    ideal: str = ""
    question: str 
    answer: str
     
@app.post("/assistant")
async def assistant_endpoint(req: AssistantRequest):
    # 파라미터 추출
    # 회사 
    company = req.company
    # 직무
    position = req.position
    # 자격요건
    qualifications = req.qualifications
    # 필수사항
    requirements = req.requirements
    # 수행업무
    duties = req.duties
    # 우대사항
    preferred = req.preferred
    # 인재상
    ideal = req.ideal
    # 질문
    question = req.question
    # 답변
    answer = req.answer

    #  assistant = openai.beta.assistants.create(
    #     name="Devcorch",
    #     instructions="You are a helpful assistant that answers user queries.",
    #     model="gpt-4o-mini",
    # )
    # 우리는 앞서 만든 assistant를 사용합니다.
    assistant = await openai.beta.assistants.retrieve("asst_jjSTOBjMS5aNgt5U8GcONkyO")

    # 유저 메세지(user prompt) 생성
    user_message = f"""
    -회사: {company}
    -직무: {position}
    -자격요건: {qualifications}
    -필수사항: {requirements}
    -수행업무: {duties}
    -우대사항: {preferred}
    -인재상: {ideal}
    
    지원자 답변 정보
    -질문: {question}
    -답변: {answer}

    ---

    아래 내용을 중심으로 평가해주세요:
    1. 이 답변이 해당 직무 및 인재상에 적합한지
    2. 보완해야 할 점이 있다면 구체적으로
    3. 가산점을 줄 수 있는 요소나 표현 제안

    친절하고 구체적으로, 면접관 또는 커리어 코치의 시선으로 피드백을 작성해주세요.
    """

    # Create a new thread with the user's message
    thread = await openai.beta.threads.create(
        messages=[{"role": "user", "content": user_message}]
    )

    # Create a run and poll until completion using the helper method
    run = await openai.beta.threads.runs.create_and_poll(
        thread_id=thread.id, assistant_id=assistant.id
    )

    # Get messages for this specific run
    messages = list(
        await openai.beta.threads.messages.list(thread_id=thread.id, run_id=run.id)
    )

    # Process the first message's content and annotations
    message_content = messages[0][1][0].content[0].text
    annotations = message_content.annotations
    citations = []

    # Replace annotations with citation markers and build citations list
    for index, annotation in enumerate(annotations):
        message_content.value = message_content.value.replace(
            annotation.text, f"[{index}]"
        )
        if file_citation := getattr(annotation, "file_citation", None):
            cited_file = await openai.files.retrieve(file_citation.file_id)
            citations.append(f"[{index}] {cited_file.filename}")

    # Combine message content with citations if any exist
    assistant_reply = message_content.value
    if citations:
        assistant_reply += "\n\n" + "\n".join(citations)
    return {"reply": assistant_reply}
  
#   print(f"Received company: {company}, position: {position}, qualifications: {qualifications}, requirements: {requirements}, duties: {duties}, preferred: {preferred}")
#   feedback = f"{req.company}의 {req.position} 직무 기준으로 첨삭을 완료했습니다."
#   return {"reply": feedback}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
