<img width="2133" height="752" alt="heroDesktopBgV2" src="https://github.com/user-attachments/assets/951af94f-ad77-4d39-9972-5762b437c8e5" />

# Track 2 - Connect AI agents to real-world data and tools using Model Context Protocol (MCP)

# 🏥 MediChat — AI Medical Assistant Agent

> An intelligent medical assistant built with Google ADK, MCP, and Gemini — deployed on Google Cloud Run.

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![Google ADK](https://img.shields.io/badge/Google-ADK-orange?logo=google)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green?logo=fastapi)
![Cloud Run](https://img.shields.io/badge/Cloud_Run-Deployed-blue?logo=googlecloud)
![MCP](https://img.shields.io/badge/MCP-Protocol-purple)

---

## Section 1 — Problem Statement & Solution

### 🔴 The Problem

Access to reliable, structured medical information remains a challenge for millions of people. Generic search engines return unstructured, often unreliable results. Patients and caregivers frequently need quick answers about symptoms, precautions, and treatment options — but without the right tool, they either turn to unreliable sources or wait for a doctor's appointment for basic informational queries.

There is also a growing need for AI agents that can connect to structured medical knowledge bases through standardized protocols, rather than relying solely on the LLM's training data, which may be outdated or imprecise.

### ✅ Our Solution

**MediChat** is an AI-powered medical assistant agent that:

- Uses **Google ADK** to orchestrate an intelligent agent powered by Gemini 1.5 Flash
- Exposes a structured medical knowledge base through the **MCP (Model Context Protocol)** — a standardized protocol for tool/data connectivity
- Provides **two specialized tools** — one for disease information and one for remedies — that the agent calls dynamically based on user intent
- Delivers responses that are clear, structured, and safe, always recommending professional medical consultation
- Is deployed on **Google Cloud Run** for scalable, serverless access via a clean chat UI

### 🎯 Key Differentiators

- Structured data retrieval via MCP tools — not just LLM hallucination
- Intent-based tool routing — the agent decides which tool to call based on the query
- Safe by design — all responses include a medical disclaimer
- Production-ready — containerized and deployed on Cloud Run

---

## Section 2 — Tech Stack, Architecture & How It Works

### 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| AI Agent Framework | Google ADK (Agent Development Kit) |
| LLM | Gemini 1.5 Flash |
| Tool Protocol | MCP (Model Context Protocol) via `fastmcp` |
| Backend API | FastAPI + Uvicorn |
| Frontend | Vanilla HTML/CSS/JS (served by FastAPI) |
| Containerization | Docker |
| Deployment | Google Cloud Run |
| Language | Python 3.12 |

### 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Google Cloud Run                      │
│                                                          │
│   ┌──────────────────────────────────────────────────┐  │
│   │               FastAPI Application                 │  │
│   │                                                   │  │
│   │   /chat ──► Chat UI (index.html)                 │  │
│   │                                                   │  │
│   │   /ask  ──► Google ADK Runner                    │  │
│   │               │                                  │  │
│   │               ▼                                  │  │
│   │         Gemini 1.5 Flash                         │  │
│   │               │                                  │  │
│   │       ┌───────┴────────┐                         │  │
│   │       ▼                ▼                         │  │
│   │  disease_info    disease_remedy                  │  │
│   │  (MCP Tool)      (MCP Tool)                      │  │
│   │       │                │                         │  │
│   │       └───────┬────────┘                         │  │
│   │               ▼                                  │  │
│   │   /mcp  ──► FastMCP Server                       │  │
│   │               │                                  │  │
│   │               ▼                                  │  │
│   │           data.json                              │  │
│   │        (10 diseases)                             │  │
│   └──────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```
---
## ⚙️ Process Flow diagram

<img width="711" height="471" alt="Untitled Diagram drawio111" src="https://github.com/user-attachments/assets/1c1bc4e2-dcbc-4342-87ef-5602fb28395f" />

---

## ⚙️ Sample Output

URL (Chat UI Endpoint):  https://medical-agent-1059652519537.us-central1.run.app/chat

<img width="1920" height="912" alt="c8e647bf-c490-4eed-a126-f651b3da7dfe" src="https://github.com/user-attachments/assets/19a0e653-f12b-401f-8529-ebca0e553f33" />

<img width="1920" height="1290" alt="2d823b2a-e28a-4026-9da7-943f51e0eeda" src="https://github.com/user-attachments/assets/ef620398-52da-4aa2-821a-c7f824c8012a" />

---

### ⚙️ How It Works

1. **User sends a query** via the chat UI (e.g., *"How do I treat dengue?"*)
2. **FastAPI `/ask` endpoint** receives the request and passes it to the ADK Runner
3. **ADK Runner** creates a session and invokes the Gemini-powered Agent
4. **Gemini analyzes the intent** — is the user asking about symptoms/info, or treatment/remedy?
5. **Agent calls the appropriate MCP tool**:
   - `disease_info` → returns symptoms, precautions, severity, transmission
   - `disease_remedy` → returns remedies, medications to avoid, when to see a doctor
6. **MCP tools query `data.json`** — a structured knowledge base of 10 common diseases
7. **Gemini synthesizes the structured data** into a clear, safe, human-readable response
8. **Response is streamed back** to the chat UI

### 📂 Project Structure

```
2-medical-mcp-agent/
├── agents/
│   ├── __init__.py
│   ├── agent.py          # ADK Agent definition
│   └── main.py           # FastAPI app + Runner + MCP mount
├── mcp_server/
│   ├── __init__.py
│   ├── tools.py          # Tool logic (data lookup)
│   └── data.json         # Structured disease knowledge base
├── static/
│   └── index.html        # Chat UI frontend
├── Dockerfile
├── requirements.txt
└── .env
```

### 🦠 Diseases Covered

The knowledge base currently covers 10 diseases:

| Disease | Info Tool | Remedy Tool |
|---|---|---|
| Dengue | ✅ | ✅ |
| Malaria | ✅ | ✅ |
| Typhoid | ✅ | ✅ |
| COVID-19 | ✅ | ✅ |
| Diabetes | ✅ | ✅ |
| Hypertension | ✅ | ✅ |
| Tuberculosis | ✅ | ✅ |
| Chickenpox | ✅ | ✅ |
| Asthma | ✅ | ✅ |
| Food Poisoning | ✅ | ✅ |

---

## Section 3 — How to Run It

### ✅ Prerequisites

- Python 3.12+
- Google Gemini API key — get one at [aistudio.google.com](https://aistudio.google.com/app/apikey)
- Git

### 📦 Installation

**1. Clone the repository**
```bash
git clone https://github.com/your-username/2-medical-mcp-agent.git
cd 2-medical-mcp-agent
```

**2. Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables**

Create a `.env` file in the root directory:
```env
GOOGLE_API_KEY=your_gemini_api_key_here
```

### 🚀 Running Locally

**Start the application:**
```bash
uvicorn agents.main:app --port 9000 --host 0.0.0.0
```

**Open the chat UI:**
```
http://127.0.0.1:9000/chat
```

**Or test via curl:**
```bash
curl -X POST http://127.0.0.1:9000/ask \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I treat dengue?"}'
```

**Access the MCP endpoint:**
```
http://127.0.0.1:9000/mcp
```

### 📋 Requirements

```txt
fastapi
uvicorn
python-dotenv
google-adk
mcp
google-genai
httpx
```

### ☁️ Deploying to Google Cloud Run

**1. Set your project variables**
```bash
export PROJECT_ID=$(gcloud config get-value project)
export REGION=us-central1
```

**2. Deploy**
```bash
gcloud run deploy medical-agent \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --port 8080 \
  --set-env-vars GOOGLE_API_KEY=your_actual_key \
  --project $PROJECT_ID
```

**3. Access your deployment**

After deployment, Cloud Run will give you a URL like:
```
https://medical-agent-xxxxxxxxxx.us-central1.run.app
```

| Endpoint | Description |
|---|---|
| `/chat` | Chat UI |
| `/ask` | POST — Agent query endpoint |
| `/mcp` | MCP protocol server |
| `/health` | Health check |

### 🔑 Environment Variables

| Variable | Description | Required |
|---|---|---|
| `GOOGLE_API_KEY` | Gemini API key from Google AI Studio | ✅ Yes |

---

## Section 4 — Future Improvements

### 🔬 Data & Knowledge

- **Expand disease database** — cover 100+ diseases, medications, and drug interactions
- **Real-time data integration** — connect to live medical APIs like WHO, CDC, or PubMed for up-to-date information
- **Multilingual support** — serve users in Tamil, Hindi, and other regional languages
- **Symptom checker** — multi-turn conversation to narrow down likely conditions from a list of symptoms

### 🤖 Agent Capabilities

- **Multi-agent architecture** — separate specialist agents for diagnosis, pharmacy, and emergency triage, orchestrated by a root agent
- **Memory across sessions** — remember patient history within a session for more contextual responses
- **Follow-up question handling** — maintain context across multiple turns for richer conversations
- **Confidence scoring** — indicate how confident the agent is in its response based on data availability

### 🏗️ Infrastructure

- **External MCP server** — move the MCP server to a dedicated Cloud Run service with proper authentication once the 421 Cloud Run routing issue is resolved upstream
- **Database backend** — replace `data.json` with Cloud Firestore or PostgreSQL for dynamic data management
- **Caching layer** — cache frequent queries with Redis to reduce Gemini API calls and latency
- **Rate limiting** — add per-user rate limiting to prevent abuse
- **Authentication** — add Google OAuth for personalized experiences

### 🎨 User Experience

- **Voice input/output** — integrate speech-to-text and text-to-speech for accessibility
- **Mobile app** — React Native app wrapping the same backend
- **Doctor referral integration** — connect to a directory of nearby doctors when severity is high
- **Emergency escalation** — detect emergency keywords and immediately surface emergency contact numbers

### 📊 Observability

- **Tracing** — integrate Google Cloud Trace for end-to-end request visibility
- **Analytics dashboard** — track most queried diseases, response quality, and usage patterns
- **Feedback loop** — thumbs up/down on responses to improve tool routing over time

---

## ⚠️ Disclaimer

MediChat is for **informational purposes only**. It is not a substitute for professional medical advice, diagnosis, or treatment. Always consult a qualified healthcare professional for medical concerns.

---

## 📄 License

MIT License — feel free to use, modify, and distribute.

---

*Built with ❤️ using Google ADK, MCP, Gemini, and FastAPI*
