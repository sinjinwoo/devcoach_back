from pathlib import Path
import inspect
import os
import json
import asyncio
from dotenv import load_dotenv
from openai import AsyncOpenAI

# =====================================================
# 0️⃣  프로젝트 루트 & company 폴더 경로  (경로 관련 추가)
# =====================================================
PROJECT_ROOT = Path(__file__).resolve().parent          # ─┐ 현재 .py 위치
COMPANY_DIR  = PROJECT_ROOT / "company"                 #   ├─ ./company
COMPANY_DIR.mkdir(exist_ok=True)                        #   └─ 없으면 생성

# =========================================
# 1) OpenAI API 키 불러오기
# =========================================
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)  # Load .env file if present

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# =========================================
# 2) System Prompt (앞서 만든 내용 그대로)
# =========================================
# Jupyter인지 여부 확인
def is_notebook():
    try:
        shell = get_ipython().__class__.__name__  # type: ignore[name-defined]
        return shell == 'ZMQInteractiveShell'
    except Exception:
        return False


def load_system_prompt_from_file() -> str | None:
    """
    prompts/system_prompt.txt 파일을 읽어 system_prompt 문자열을 반환한다.
    경로 오류 또는 파일 내용이 비어 있으면 None 반환.
    """
    try:
        # 현재 프로젝트 루트 계산
        if is_notebook():
            ROOT_DIR = Path().resolve()
        else:
            ROOT_DIR = Path(inspect.getfile(lambda: None)).resolve().parent

        # 프롬프트 경로 설정
        prompt_path = ROOT_DIR / "prompts" / "system_prompt.txt"

        # 파일 읽기 및 내용 확인
        if not prompt_path.exists():
            print(f"[경고] 파일 없음: {prompt_path}")
            return None

        with prompt_path.open("r", encoding="utf-8") as fp:
            content = fp.read().strip()
            return content if content else None

    except Exception as e:
        print(f"[에러] system_prompt 로딩 실패: {e}")
        return None

# ─────────────────────────────────────────
# 3)  GPT 호출 함수   (openai-python 1.x 스타일)
# ─────────────────────────────────────────
async def call_openai_assistant_api(
        text1: str,
        text2: str,
        system_prompt: str,
        user_prompt_prefix: str = "다음 두 텍스트를 분석해 규칙에 맞게 구조화해줘.",
        model: str = "gpt-4o-mini"
    ) -> dict:
    """
    두 텍스트를 GPT-4o-mini에 전달 후 JSON 결과 반환
    """

    user_prompt = f"""{user_prompt_prefix}
    
    <텍스트 파일1>
    {text1}
    
    <텍스트 파일2>
    {text2}""".strip()

    try:
        response = await openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user",    "content": user_prompt}
            ],
            temperature=0.2
        )

        reply = response.choices[0].message.content.strip()

        try:
            print(reply)
            return json.loads(reply)
        except json.JSONDecodeError:
            print("⚠️ JSON 파싱 실패 – 원본 문자열 반환")
            return {"raw_response": reply}

    except Exception as e:
        return {"error": str(e)}


# ─────────────────────────────────────────
# 4)  회사별 직무 JSON 추출 함수 (Async)
# ─────────────────────────────────────────
async def fetch_job_json_by_company(company_name: str) -> list[dict] | None:
    """
    주어진 회사명 기반으로 원문/ocr 텍스트를 읽고 GPT 호출하여
    구조화된 직무 JSON 리스트를 반환합니다.

    - 입력:
        company_name: "회사명" (확장자 없이, 예: '(주)지아이티')
    - 반환:
        job_list: [{...}, {...}, ...] 형식의 리스트 (성공 시)
        None: system_prompt 없음 또는 에러 발생 시
    """
    # 1. system_prompt 불러오기
    system_prompt = load_system_prompt_from_file()
    if system_prompt is None:
        print("❌ [에러] system_prompt.txt 를 찾을 수 없거나 비어 있습니다.")
        return None

    # 2. 파일 경로 설정 및 텍스트 읽기 (company/ 폴더 기준)
    try:
        file1_path = COMPANY_DIR / f"{company_name}.txt"
        file2_path = COMPANY_DIR / f"{company_name}_ocr.txt"

        with file1_path.open("r", encoding="utf-8") as f1:
            txt1 = f1.read()

        with file2_path.open("r", encoding="utf-8") as f2:
            txt2 = f2.read()

    except FileNotFoundError as e:
        print(f"❌ [에러] 텍스트 파일 누락: {e}")
        return None

    # 3. GPT 호출 (await 사용!)
    result = await call_openai_assistant_api(txt1, txt2, system_prompt)

    # 4. 결과 검증 및 반환
    if isinstance(result, dict) and "error" in result:
        print(f"❌ [API 호출 실패] {result['error']}")
        return None

    if isinstance(result, dict) and "raw_response" in result:
        print("⚠️ [경고] JSON 파싱 실패 – 원본 문자열로 반환됨")
        return None

    # 5. 정상 JSON 데이터 반환
    return result  # type: ignore[return-value]


# ─────────────────────────────────────────
# 5)  테스트 실행 (스크립트 직접 실행 시)
# ─────────────────────────────────────────
if __name__ == "__main__":
    # 예시 회사명: (주)지아이티
    company = "(주)지아이티"

    # asyncio.run 을 사용해 비동기 함수 실행
    job_list = asyncio.run(fetch_job_json_by_company(company))

    if job_list:
        print(json.dumps(job_list, ensure_ascii=False, indent=2))
    else:
        print("⚠️ 직무 데이터 로딩 실패")
