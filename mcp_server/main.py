from mcp.server.fastmcp import FastMCP
from mcp_server.tools import get_disease_info, get_disease_remedy

# ✅ This creates a real MCP server, not plain FastAPI
mcp = FastMCP("MedicalMCPServer")


@mcp.tool()
def disease_info(disease: str) -> dict:
    """Get information about a disease including symptoms and causes."""
    return get_disease_info(disease)


@mcp.tool()
def disease_remedy(disease: str) -> dict:
    """Get treatment and remedy information for a disease."""
    return get_disease_remedy(disease)


# ✅ Export the ASGI app so uvicorn can serve it
app = mcp.streamable_http_app()

# ```

# ---

# **Step 3 — Update `.env`**

# Since you're on GCP Cloud Shell, the URL must include `/mcp` at the end:
# ```
# MCP_BASE_URL=https://8000-cs-71486fb0-e482-4a53-9ba6-b6713dfe9a57.cs-asia-southeast1-seal.cloudshell.dev/mcp


# from fastapi import FastAPI
# from pydantic import BaseModel
# from mcp_server.tools import get_disease_info, get_disease_remedy

# app = FastAPI()


# class DiseaseRequest(BaseModel):
#     disease: str


# @app.get("/")
# def root():
#     return {"message": "MCP Medical Server Running"}


# # Tool 1: Info
# @app.post("/tools/get_disease_info")
# def disease_info(req: DiseaseRequest):
#     return get_disease_info(req.disease)


# # Tool 2: Remedy
# @app.post("/tools/get_disease_remedy")
# def disease_remedy(req: DiseaseRequest):
#     return get_disease_remedy(req.disease)