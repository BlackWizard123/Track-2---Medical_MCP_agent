import os
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
import uuid

from dotenv import load_dotenv
load_dotenv()


from agents.agent import build_agent

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
agent = build_agent()


# ✅ Set up session service and runner
session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="MedicalAgent",
    session_service=session_service
)

class QueryRequest(BaseModel):
    query: str


# @app.get("/")
# def root():
#     return {"message": "ADK Medical Agent Running"}

@app.get("/")
def chat_ui():
    return FileResponse("static/index.html")

@app.post("/ask")
async def ask(req: QueryRequest):
    # ✅ Create a unique session per request
    session_id = str(uuid.uuid4())
    user_id = "user"

    await session_service.create_session(
        app_name="MedicalAgent",
        user_id=user_id,
        session_id=session_id
    )

    # ✅ Wrap the query in the proper Content/Part format
    message = Content(parts=[Part(text=req.query)], role="user")

    response_text = ""

    async for event in runner.run_async(
        user_id=user_id,
        session_id=session_id,
        new_message=message
    ):
        if event.is_final_response():
            if event.content and event.content.parts:
                response_text = event.content.parts[0].text
                break

    return {"response": response_text}

# from fastapi import FastAPI
# from pydantic import BaseModel

# from agents.agent import build_agent

# app = FastAPI()

# agent = build_agent()


# class QueryRequest(BaseModel):
#     query: str


# @app.get("/")
# def root():
#     return {"message": "ADK Medical Agent Running"}


# @app.post("/ask")
# async def ask(req: QueryRequest):
#     response_text = ""

#     async for event in agent.run_live(req.query):
#         if hasattr(event, "content") and event.content:
#             response_text += event.content

#     return {
#         "response": response_text
#     }

