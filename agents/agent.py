import os
from dotenv import load_dotenv

from google.adk.agents import Agent
# from google.adk.tools.mcp_tool import McpToolset
# from google.adk.tools.mcp_tool import McpToolset
from google.adk.tools.mcp_tool import MCPToolset, StreamableHTTPConnectionParams

# Load env
load_dotenv()

# Configure Gemini
# genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# MCP Server URL (important)
MCP_SERVER_URL = os.getenv("MCP_BASE_URL")
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")


def build_agent():
    # 🔥 Connect to MCP server
    # mcp_tools = McpToolset(url="http://127.0.0.1:8000")
    mcp_tools = MCPToolset(
        connection_params=StreamableHTTPConnectionParams(
            url=MCP_SERVER_URL,
        )
    )

    # 🧠 Create ADK Agent
    agent = Agent(
        name="MedicalAgent",
        model="gemini-2.5-flash",
        tools=[mcp_tools],   
        description="""
You are a medical assistant.

- Use available tools when needed.
- If user asks about symptoms or info → use info tool.
- If user asks about treatment → use remedy tool.
- Always give safe, non-diagnostic answers.
- Add disclaimer: consult a doctor.
- Try to elaborate to make it better understandable.

Be clear and structured.
"""
    )

    return agent