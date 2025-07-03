# thread_manager.py
import uuid
from typing import Dict
from openai import AsyncOpenAI
openai = AsyncOpenAI()

_thread_map: Dict[str, str] = {}          # {session_key: thread_id}

def new_session_key() -> str:
    return str(uuid.uuid4())

async def get_or_create_thread(session_key: str) -> str:
    if session_key in _thread_map:
        return _thread_map[session_key]

    thread = await openai.beta.threads.create()  # 빈 Thread
    _thread_map[session_key] = thread.id
    return thread.id