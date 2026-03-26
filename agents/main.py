import os
from dotenv import load_dotenv
load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai.types import Content, Part
from mcp.server.fastmcp import FastMCP
from mcp_server.tools import get_disease_info, get_disease_remedy
import uuid
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ MCP server still mounted — satisfies requirement #2
mcp = FastMCP("MedicalMCPServer")

@mcp.tool()
def disease_info(disease: str) -> dict:
    """Get information about a disease including symptoms and causes."""
    return get_disease_info(disease)

@mcp.tool()
def disease_remedy(disease: str) -> dict:
    """Get treatment and remedy information for a disease."""
    return get_disease_remedy(disease)

app.mount("/mcp", mcp.streamable_http_app())
app.mount("/static", StaticFiles(directory="static"), name="static")

# ✅ ADK agent uses the same functions directly — no HTTP roundtrip
def get_disease_info_tool(disease: str) -> dict:
    """Get information about a disease including symptoms, precautions and severity."""
    return get_disease_info(disease)

def get_disease_remedy_tool(disease: str) -> dict:
    """Get treatment and remedy information for a disease."""
    return get_disease_remedy(disease)

agent = Agent(
    name="MedicalAgent",
    model="gemini-2.5-flash",
    tools=[get_disease_info_tool, get_disease_remedy_tool],
    description="""
You are a medical assistant.
- Use get_disease_info_tool for symptoms, precautions, severity.
- Use get_disease_remedy_tool for treatments and remedies.
- Always give safe, non-diagnostic answers.
- Add disclaimer: consult a doctor.
Be clear and structured.
"""
)

session_service = InMemorySessionService()
runner = Runner(
    agent=agent,
    app_name="MedicalAgent",
    session_service=session_service
)

class QueryRequest(BaseModel):
    query: str

@app.get("/")
def root():
    return {"message": "ADK Medical Agent Running"}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/chat")
def chat_ui():
    return FileResponse("static/index.html")

@app.post("/ask")
async def ask(req: QueryRequest):
    session_id = str(uuid.uuid4())
    user_id = "user"

    try:
        await session_service.create_session(
            app_name="MedicalAgent",
            user_id=user_id,
            session_id=session_id
        )

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

    except Exception as e:
        logger.error(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

        
# --------------------------------------------
# import os
# from dotenv import load_dotenv
# load_dotenv()
# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from pydantic import BaseModel
# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from google.genai.types import Content, Part
# import uuid
# import logging

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")

# @app.get("/chat")
# def chat_ui():
#     return FileResponse("static/index.html")

# # ✅ Don't build agent at module level — only when first request comes in
# session_service = InMemorySessionService()
# _runner = None

# def get_runner():
#     global _runner
#     if _runner is None:
#         from agents.agent import build_agent
#         agent = build_agent()
#         _runner = Runner(
#             agent=agent,
#             app_name="MedicalAgent",
#             session_service=session_service
#         )
#     return _runner

# class QueryRequest(BaseModel):
#     query: str

# @app.get("/")
# def root():
#     return {"message": "ADK Medical Agent Running"}

# @app.get("/health")
# def health():
#     # ✅ Fast health check — no MCP connection needed
#     return {"status": "ok"}

# @app.post("/ask")
# async def ask(req: QueryRequest):
#     session_id = str(uuid.uuid4())
#     user_id = "user"

#     try:
#         await session_service.create_session(
#             app_name="MedicalAgent",
#             user_id=user_id,
#             session_id=session_id
#         )

#         message = Content(parts=[Part(text=req.query)], role="user")
#         response_text = ""

#         async for event in get_runner().run_async(
#             user_id=user_id,
#             session_id=session_id,
#             new_message=message
#         ):
#             if event.is_final_response():
#                 if event.content and event.content.parts:
#                     response_text = event.content.parts[0].text
#                     break

#         return {"response": response_text}

#     except Exception as e:
#         logger.error(f"Error: {e}")
#         raise HTTPException(status_code=500, detail=str(e))

# --------------------------------------------------

# import os
# from fastapi import FastAPI
# from pydantic import BaseModel
# from fastapi.staticfiles import StaticFiles
# from fastapi.responses import FileResponse
# from fastapi.middleware.cors import CORSMiddleware

# from google.adk.runners import Runner
# from google.adk.sessions import InMemorySessionService
# from google.genai.types import Content, Part
# import uuid

# from dotenv import load_dotenv
# load_dotenv()


# from agents.agent import build_agent

# app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# app.mount("/static", StaticFiles(directory="static"), name="static")

# os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")
# agent = build_agent()


# # ✅ Set up session service and runner
# session_service = InMemorySessionService()
# runner = Runner(
#     agent=agent,
#     app_name="MedicalAgent",
#     session_service=session_service
# )

# class QueryRequest(BaseModel):
#     query: str


# # @app.get("/")
# # def root():
# #     return {"message": "ADK Medical Agent Running"}

# @app.get("/")
# def chat_ui():
#     return FileResponse("static/index.html")

# @app.post("/ask")
# async def ask(req: QueryRequest):
#     # ✅ Create a unique session per request
#     session_id = str(uuid.uuid4())
#     user_id = "user"

#     await session_service.create_session(
#         app_name="MedicalAgent",
#         user_id=user_id,
#         session_id=session_id
#     )

#     # ✅ Wrap the query in the proper Content/Part format
#     message = Content(parts=[Part(text=req.query)], role="user")

#     response_text = ""

#     async for event in runner.run_async(
#         user_id=user_id,
#         session_id=session_id,
#         new_message=message
#     ):
#         if event.is_final_response():
#             if event.content and event.content.parts:
#                 response_text = event.content.parts[0].text
#                 break

#     return {"response": response_text}

# -------------------------------------------------------
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

