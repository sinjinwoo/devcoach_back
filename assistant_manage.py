"""
assistant_manager.py
~~~~~~~~~~~~~~~~~~~~
OpenAI Assistant ID를 관리하기 위한 유틸리티 모듈입니다.

주요 기능
---------
1. **load_assistant_id()**
   `.assistant.id` 파일에서 Assistant ID를 읽어 반환합니다(없으면 ``None``).
2. **create_assistant()**
   `prompts/assistant_prompt.txt`에 정의된 시스템 프롬프트를 사용해 새로운 Assistant를 생성하고
   그 ID를 `.assistant.id`에 저장합니다.
3. **delete_assistant()**
   `.assistant.id`에 기록된 Assistant를 삭제하고 해당 파일도 제거합니다.
4. **get_or_create_assistant()**
   Assistant가 이미 있으면 그대로 사용하고, 없거나 ID가 잘못됐으면 새로 생성합니다.

파일 맨 아래에는 개발자가 로컬에서 빠르게 테스트할 수 있는 간단한 CLI가 포함돼 있습니다.
"""

import os
import asyncio
from pathlib import Path
from typing import Optional

from openai import AsyncOpenAI
from openai import NotFoundError, OpenAIError
from dotenv import load_dotenv

# ---------------------------------------------------------------------------
# 비동기 OpenAI 클라이언트(모듈당 한 번만 초기화)
# ---------------------------------------------------------------------------
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path) # Load .env file if present

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# ---------------------------------------------------------------------------
# 상수 및 경로 설정
# ---------------------------------------------------------------------------
ASSISTANT_FILE = ".assistant.id"               # Assistant ID를 저장할 파일
PROMPT_FILE    = "prompts/assistant_prompt.txt" # 시스템 프롬프트 위치
KEY_NAME       = "OPENAI_ASSISTANT_ID"          # .assistant.id 파일 내 키 이름

# 현재 파일 기준 프로젝트 루트 경로
PROJECT_ROOT = Path(__file__).resolve().parent

# ---------------------------------------------------------------------------
# Helper: 로컬 Assistant ID 읽기
# ---------------------------------------------------------------------------

def load_assistant_id(file_path: Path = PROJECT_ROOT / ASSISTANT_FILE) -> Optional[str]:
    """`file_path`에서 Assistant ID를 읽어 반환합니다. 없으면 ``None``."""
    if not file_path.exists():
        return None

    with file_path.open("r", encoding="utf-8") as fin:
        for line in fin:
            if line.startswith(f"{KEY_NAME}="):
                return line.strip().split("=", 1)[1]
    return None

# ---------------------------------------------------------------------------
# Helper: 새 Assistant 생성 후 ID 저장
# ---------------------------------------------------------------------------

async def create_assistant(
    prompt_path: Path = PROJECT_ROOT / PROMPT_FILE,
    file_path: Path = PROJECT_ROOT / ASSISTANT_FILE,
) -> str:
    """시스템 프롬프트로 새 Assistant를 만들고 ID를 파일에 저장합니다."""

    if not prompt_path.exists():
        raise FileNotFoundError(f"시스템 프롬프트 파일이 없습니다: {prompt_path}")

    system_prompt = prompt_path.read_text(encoding="utf-8")

    assistant = await openai.beta.assistants.create(
        name="Devcorch",
        instructions=system_prompt,
        model="gpt-4o-mini",
    )

    # 새 ID 파일에 기록
    with file_path.open("w", encoding="utf-8") as fout:
        fout.write(f"{KEY_NAME}={assistant.id}\n")

    print(f"🆕 Assistant 생성 완료: {assistant.id}")
    return assistant.id

# ---------------------------------------------------------------------------
# Helper: 기존 Assistant 삭제
# ---------------------------------------------------------------------------

async def delete_assistant(file_path: Path = PROJECT_ROOT / ASSISTANT_FILE) -> None:
    """`.assistant.id`에 기록된 Assistant를 삭제하고 파일을 제거합니다."""

    assistant_id = load_assistant_id(file_path)
    if not assistant_id:
        print("⚠️  삭제할 Assistant ID가 없습니다.")
        return

    try:
        await openai.beta.assistants.delete(assistant_id)
        file_path.unlink(missing_ok=True)
        print(f"🗑️  Assistant {assistant_id} 삭제 및 파일 제거 완료.")
    except OpenAIError as exc:
        print(f"❌ Assistant 삭제 중 오류 발생: {exc}")

# ---------------------------------------------------------------------------
# Public: Assistant ID 가져오기(없으면 생성)
# ---------------------------------------------------------------------------

async def get_or_create_assistant() -> str:
    """유효한 Assistant ID를 반환합니다(필요 시 자동 생성)."""

    assistant_id = load_assistant_id()
    if assistant_id:
        try:
            # ID가 실제로 존재하는지 확인
            await openai.beta.assistants.retrieve(assistant_id)
            print(f"✅ 기존 Assistant 사용: {assistant_id}")
            return assistant_id
        except NotFoundError:
            print("⚠️  저장된 Assistant ID가 유효하지 않습니다. 새로 생성합니다…")
        except OpenAIError as exc:
            raise RuntimeError(f"Assistant 확인 중 오류: {exc}") from exc

    # ID가 없거나 무효 → 새로 생성
    return await create_assistant()

# ---------------------------------------------------------------------------
# 개발자용 간단한 CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    """로컬에서 각 기능을 빠르게 시험해볼 수 있는 CLI."""

    MENU = (
        "\nAssistant Manager CLI"  # 제목
        "\n----------------------"
        "\n1. Assistant ID 읽기"
        "\n2. Assistant 새로 생성"
        "\n3. Assistant 가져오기(필요 시 생성)"
        "\n0. Assistant 삭제"
        "\nq. 종료"
        "\n"
    )

    while True:
        choice = input(MENU + "원하는 번호를 선택하세요: ").strip().lower()

        if choice == "1":
            aid = load_assistant_id()
            print(f"→ Assistant ID: {aid or '없음 (.assistant.id 파일 없음)'}")
        elif choice == "2":
            aid = asyncio.run(create_assistant())
            print(f"→ 생성된 ID: {aid}")
        elif choice == "3":
            aid = asyncio.run(get_or_create_assistant())
            print(f"→ 현재 사용 중인 ID: {aid}")
        elif choice == "0":
            asyncio.run(delete_assistant())
        elif choice == "q":
            print("CLI를 종료합니다. 안녕히 가세요! ✨")
            break
        else:
            print("잘못된 입력입니다. 0, 1, 2, 3 또는 q 중에서 선택하세요.")
