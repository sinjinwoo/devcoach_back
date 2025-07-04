import os
from openai import AsyncOpenAI
from openai import OpenAIError
from thread_manager import get_or_create_thread   # ← 추가

# 비동기 클라이언트
openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

async def run_assistant(
    assistant_id: str,
    request_data: dict,
    session_key: str,                   # ← 세션키를 인자로 받음
) -> str:
    """
    assistant_id와 request_data를 받아, user_message를 구성하고 Assistant API를 호출한 뒤
    응답을 문자열로 반환합니다.

    Parameters
    ----------
    assistant_id : str
        사용할 Assistant의 ID
    request_data : dict
        FastAPI 요청 데이터(Pydantic 모델의 .dict())
    session_key : str
        브라우저 세션(쿠키)과 매핑된 키. thread_id를 얻기 위해 사용.

    Returns
    -------
    str
        Assistant의 응답 메시지
    """
    # 0️⃣ thread 확보 (없으면 새로 생성)
    thread_id = await get_or_create_thread(session_key)

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

너는 지원자가 지원하는 {request_data['company']} 회사의 10년차 인사담당자야. 지원자의 답변이 질문의 의도에 맞게 잘 작성되었는지 좋은 점이나 나쁜 점을 피드백해줘.

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
        # 2️⃣ (변경) 기존 Thread에 메시지 추가
        await openai.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=user_message,
        )

        # 3️⃣ Run 생성 및 완료될 때까지 대기
        run = await openai.beta.threads.runs.create_and_poll(
            thread_id=thread_id,
            assistant_id=assistant_id,
        )

        # 4️⃣ Run 결과에서 메시지 가져오기
        messages = await openai.beta.threads.messages.list(
            thread_id=thread_id,
            run_id=run.id,
        )

        # 첫 번째 메시지 내용 추출
        reply_text = messages.data[0].content[0].text.value

        return reply_text.strip()

    except OpenAIError as exc:
        raise RuntimeError(f"Assistant 실행 중 오류: {exc}") from exc