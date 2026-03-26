FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY agents/ ./agents/
COPY mcp_server/ ./mcp_server/
COPY static/ ./static/
EXPOSE 8080
CMD ["uvicorn", "agents.main:app", "--host", "0.0.0.0", "--port", "8080"]