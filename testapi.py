# pip install fastapi uvicorn openai python-dotenv
from fastapi import FastAPI, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from openai import AsyncOpenAI
import uuid
import os
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware
from crawling import fetch_recruitment_info,convert_to_recruitment_info, fetch_and_store_job_content
from fastapi import Query
from pathlib import Path
from job_gpt import fetch_job_json_by_company
from image_ocr import perform_ocr_to_txt_auto
from assistant_manage import get_or_create_assistant  # 기존 assistant ID 로더
from assistant_service  import run_assistant           # thread 재사용 버전


env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path) # Load .env file if present

openai = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

# -----------------------------------------
# 앱 기동 시 ➊ assistant ID 확보
# -----------------------------------------
ASSISTANT_ID: str | None = None      # 전역에 보관
SESSION_COOKIE = "thread_cookie"     # 쿠키 이름

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
    """
    프론트에서 입력받은 회사명을 가지고 웹크롤링 해서
    모집공고 데이터를 뽑아주는 함수
    """
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
    """
    프론트에서 입력받은 회사명, url을 바탕으로 웹크롤링을 하여
    텍스트 또는 이미지 파일을 ocr 과정을 통해
    직무 종류 데이터를 뽑아주는 함수
    """
    
    # 회사
    company = req.company
    # url
    url = req.url

    fetch_and_store_job_content(url, company) # 직무 txt파일로 뽑기

    is_ocr_success = perform_ocr_to_txt_auto(company) # 이미지파일 직무 txt파일로 뽑기

    if is_ocr_success == None:
        print('ocr 된 게 없습니다.')

    job_list = await fetch_job_json_by_company(company)
    if job_list == None:
        return {"message" : "None"}
    else:
        return {"reply" : job_list}

@app.on_event("startup")
async def startup_event():
    global ASSISTANT_ID
    ASSISTANT_ID = await get_or_create_assistant()

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

# -----------------------------------------
# POST /assistant
# -----------------------------------------
@app.post("/assistant")
async def assistant_endpoint(body: AssistantRequest,
                             thread_cookie: str | None = Cookie(default=None)):
    """
    • 쿠키에 thread_cookie가 있으면 세션키로 사용  
    • 없으면 새 UUID → thread_manager가 새 thread 생성  
    • 세션키를 run_assistant()에 넘겨 동일 thread 유지
    """

    # 0) 세션키 결정(없으면 새로 만듦)
    session_key = thread_cookie or str(uuid.uuid4())

    # 1) Assistant 호출
    reply = await run_assistant(ASSISTANT_ID, body.dict(), session_key)

    # 2) 쿠키 세팅(최초 호출 시만)
    resp = JSONResponse({"reply": reply})
    if thread_cookie is None:                 # 새 세션이면
        resp.set_cookie(
            key=SESSION_COOKIE,
            value=session_key,
            max_age=60 * 60 * 24,             # 24h
            path="/",
            secure=True,                      # HTTPS 배포 환경이면 True
            httponly=True,                    # JS에서 읽을 수 없도록
            samesite="lax",
        )
    return resp     

  
#   print(f"Received company: {company}, position: {position}, qualifications: {qualifications}, requirements: {requirements}, duties: {duties}, preferred: {preferred}")
#   feedback = f"{req.company}의 {req.position} 직무 기준으로 첨삭을 완료했습니다."
#   return {"reply": feedback}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)