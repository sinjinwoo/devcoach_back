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


    return {"reply": 1}

class AssistantRequest(BaseModel):
    company: str
    position: str
    qualifications: str = ""
    requirements: str = ""
    duties: str = ""
    preferred: str = ""

@app.post("/assistant")
async def assistant_endpoint(req: AssistantRequest):
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

    print(f"Received company: {company}, position: {position}, qualifications: {qualifications}, requirements: {requirements}, duties: {duties}, preferred: {preferred}")

    return {"reply": 1}

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
