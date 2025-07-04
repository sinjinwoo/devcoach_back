"""
assistant_service.py
~~~~~~~~~~~~~~~~~~~~
OpenAI Assistant를 실행하고 결과를 반환하는 모듈

Features
--------
- run_assistant()
    주어진 assistant_id와 request_data로 user_message를 생성하여
    Assistant API를 호출하고, 응답을 문자열로 반환합니다.
"""

import os
from openai import AsyncOpenAI
from openai.error import OpenAIError

# 비동기 클라이언트
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_assistant(assistant_id: str, request_data: dict) -> str:
    """
    assistant_id와 request_data를 받아, user_message를 구성하고 Assistant API를 호출한 뒤
    응답을 문자열로 반환합니다.

    Parameters
    ----------
    assistant_id : str
        사용할 Assistant의 ID
    request_data : dict
        FastAPI 요청 데이터(Pydantic 모델의 .dict())

    Returns
    -------
    str
        Assistant의 응답 메시지
    """

    # 1️⃣ user_message 구성
    user_message = f"""
- 회사: {request_data['company']}
- 직무: {request_data['position']}
- 자격요건: {request_data['qualifications']}
- 필수사항: {request_data['requirements']}
- 수행업무: {request_data['duties']}
- 우대사항: {request_data['preferred']}
- 인재상: {request_data['ideal']}

지원자 답변 정보
- 질문: {request_data['question']}
- 답변: {request_data['answer']}

---

너는 지원자가 지원하는 {company}회사의 10년차 인사담당자야. 지원자의 답장이 질문의 의도에 맞게 잘 작성되었는지 좋은 점이나 나쁜 점을 피드백해줘.

사용자가 작성한 질문을 중심으로 다음의 내용을 참고하여 사용자의 답변이 질문의 의도에 맞게 작성되어 있는지 피드백 해줘.

회사의 지원동기를 묻는 질문의 경우 회사의 주요 내용(사업,업무,제도,최근 이슈) 등을 기술하여 작성했는지 판단하여 피드백 해줘.

생각하게 된 이유, 사건, 경험에 대해서 묻는 질문은 꼭 관련 경험이 함께 작성되어있는지 판단하여 피드백 해줘.



아래 내용을 중심으로 평가해주세요:
1. 이 답변이 해당 직무 및 인재상에 적합한지
2. 보완해야 할 점이 있다면 구체적으로
3. 가산점을 줄 수 있는 요소나 표현 제안

친절하고 구체적으로, 면접관 또는 커리어 코치의 시선으로 피드백을 작성해주세요.
"""

    try:
        # 2️⃣ 새로운 Thread 생성
        thread = await openai.beta.threads.create(
            messages=[{"role": "user", "content": user_message}]
        )

        # 3️⃣ Run 생성 및 완료될 때까지 대기
        run = await openai.beta.threads.runs.create_and_poll(
            thread_id=thread.id,
            assistant_id=assistant_id,
        )

        # 4️⃣ Run 결과에서 메시지 가져오기
        messages = await openai.beta.threads.messages.list(
            thread_id=thread.id,
            run_id=run.id,
        )

        # 첫 번째 메시지 내용 추출
        reply_text = messages.data[0].content[0].text.value

        return reply_text.strip()

    except OpenAIError as exc:
        raise RuntimeError(f"Assistant 실행 중 오류: {exc}") from exc

# =====================================================
# 6️⃣  CLI: RAGAS 평가용 실행 (assistant_service.py 직접 실행 시)
# =====================================================
if __name__ == "__main__":
    import asyncio
    from pathlib import Path
    import json

    # ① assistant_id 로드 (.assistant.id 파일에 저장돼 있다고 가정)
    assistant_id_path = Path(".assistant.id")
    if not assistant_id_path.exists():
        raise FileNotFoundError("⚠️ .assistant.id 파일을 찾을 수 없습니다!")
    raw_id= assistant_id_path.read_text(encoding="utf-8").strip()
    assistant_id = raw_id.split("=", 1)[-1]

    # ② request_data 템플릿 (직무 JSON + question/answer 빈 칸)
    job_json_str = """
[
  {
    "직무명": "Tech PM(Project Manager)",
    "담당업무": [
      "현대 / 기아 자동차 공장 내 생산 차량에 대한 검사 설비 개발",
      "검사 설비 개발 사양 분석",
      "검사 설비 S/W 개발 (UI 및 제어 프로그램 개발)",
      "검차 설비 구축 및 외부 장비와의 인터페이스 구성",
      "검차 설비 운영 및 유지보수",
      "생산 라인 내 설비 이슈 진단 및 문제 해결",
      "고객(공장 측)과의 현장 대응 및 기술 지원"
    ],
    "자격요건": [
      "C++, C# 등 프로그래밍 언어 사용 가능자",
      "관련 프로그램 개발 경험 보유자 (경력 무관, 실무 중심이면 가능)"
    ],
    "필수사항": [
      "C++, C# 등 프로그래밍 언어 사용 가능자",
      "관련 프로그램 개발 경험 보유자 (경력 무관, 실무 중심이면 가능)"
    ],
    "우대사항": [
      "컴퓨터, 전자, 제어, 로봇, 소프트웨어공학 등 관련 전공자",
      "자동차 검차 설비에 대한 이해 보유자 (※ 경험이 없어도 실무를 통해 역량 향상 가능)",
      "자동차 통신 프로토콜(CAN, KWP 등) 이해",
      "진단기 및 진단 장비 활용 경험"
    ],
    "인재상": [
      "열정과 도전, 소통과 협력, 창의와 혁신, 학습과 성장"
    ]
  }
]
""".strip()
    
    job_list = json.loads(job_json_str)        # 리스트 형태
    first_job = job_list[0]                    # 여기서는 첫 번째 직무만 사용
    # ③ request_data 딕셔너리 구성
    request_data: dict = {
        "company": "예시회사",                      # 필요 시 수정
        "position": first_job["직무명"],
        "qualifications": "\n".join(first_job["자격요건"]),
        "requirements":   "\n".join(first_job["필수사항"]),
        "duties":         "\n".join(first_job["담당업무"]),
        "preferred":      "\n".join(first_job["우대사항"]),
        "ideal":          "\n".join(first_job["인재상"]),
        # -------------- 질문 / 답변 (빈 값) --------------
        "question": "",
        "answer":   "",
    }

    # ④ 사용자에게 질문/답변 직접 입력받기 (원할 경우)
    print("📝 지원자 질문/답변을 입력하세요. (그냥 Enter 치면 빈 값 유지)")
    q_in = input("질문: ").strip()
    a_in = input("답변: ").strip()
    if q_in:
        request_data["question"] = q_in
    if a_in:
        request_data["answer"] = a_in

    # ⑤ 세션키는 간단히 company 이름을 사용 (테스트용)
    session_key = request_data["company"]

    # ⑥ Assistant 실행
    reply = asyncio.run(
        run_assistant(assistant_id, request_data, session_key)
    )

    print("\n========== Assistant 응답 ==========")
    print(reply)