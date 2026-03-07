# Weather API Agent

An intelligent AI agent
that answers to user queries
and 
first it checks from the given files context 
then search the web using DuckDuckGo

API Integration
can fetch real-time weather data via OpenWeatherMap API 




## Features

- **Local AI Model**: Runs on Ollama (llama3.2) - no cloud API costs
- **Real-time Weather**: Fetches current weather for any city worldwide
- **Web Search**: Falls back to DuckDuckGo search for general queries
- **File Context**: Can read and analyze local files you provide
- **ReAct Agent**: Autonomously decides which tool to use based on your query


Summary
LLM outputs a tool call as part of its response.
Agent framework detects and executes the tool call.
Tool output is returned to the LLM for final answer generation.



## Quick Start

### 1. Prerequisites

```bash
# Install Ollama
brew install ollama  # macOS
# or visit: https://ollama.ai

# Pull the model
ollama pull llama3.2

# Start Ollama server
ollama serve
```

### 2. Setup

```bash
# Clone the repo
git clone https://github.com/gpavankumarnov/whether-api-agent.git
cd whether-api-agent

# Copy environment template
cp .env.example .env

# Add your OpenWeatherMap API key to .env
# Get free key: https://openweathermap.org/api
```

### 3. Run

```bash
# Install dependencies and run
uv run main.py --query "What's the weather in Delhi?"

# With file context
uv run main.py --query "Explain this code" --files main.py
```

## How It Works

```
User Query
    ↓
Agent (Ollama llama3.2)
    ↓
Decides which tool to use:
    ├─ Weather query? → weather_api(city)
    ├─ General query? → web_search(query)
    └─ File provided? → Read file context
    ↓
Returns formatted answer
```

### Example Flow

**Query:** "What's the weather in Mumbai?"

1. Agent receives query
2. Recognizes it's a weather request
3. Calls `weather_api("Mumbai")`
4. OpenWeatherMap returns: temp, humidity, wind
5. Agent formats and presents the answer

## Project Structure

```
.
├── main.py           # Main agent logic
├── .env              # Your API keys (not in git)
├── .env.example      # Template for .env
├── pyproject.toml    # Dependencies
└── README.md         # This file
```

## Tools Available

| Tool | Purpose | Example |
|------|---------|---------|
| `weather_api` | Real-time weather data | "Delhi weather today" |
| `web_search` | General web search | "Latest Python news" |
| `read_context_files` | Analyze local files | `--files main.py` |

## Tech Stack

- **LangChain** - Agent framework
- **LangGraph** - ReAct agent orchestration
- **Ollama** - Local LLM runtime
- **OpenWeatherMap API** - Weather data
- **DuckDuckGo** - Web search

## License

MIT



----------------- Testing --------------------------


🧪 Test Scenarios

Scenario 1: Ask about file content

Q:
uv run main.py --query "What are the main topics covered in this file?" --files test_files/python_basics.txt

Expected: Agent summarizes Python basics (variables, functions, loops, etc.)



Scenario 2: Compare weather data with real-time API

Q:
uv run main.py --query "Compare the Delhi temperature in the file with current weather" --files test_files/weather_data.txt

Expected: Agent reads file data AND calls weather_api("Delhi") to compare




Scenario 3: Code explanation

Q:
uv run main.py --query "Explain what this code does and how it works" --files test_files/code_snippet.py

Expected: Agent analyzes the WeatherAnalyzer class and explains its methods



Scenario 4: Multiple files

Q:
uv run main.py --query "What's the relationship between these files?" --files test_files/python_basics.txt test_files/code_snippet.py

Expected: Agent reads both files and explains how the code uses Python concepts



Scenario 5: Extract specific info

Q:
uv run main.py --query "What are the error codes in the API documentation?" --files test_files/api_documentation.txt

Expected: Agent extracts and lists error codes (400, 401, 404, 500)



Scenario 6: Weather query without file (baseline)

Q:
uv run main.py --query "What's the weather in Mumbai today?"

Expected: Agent uses weather_api tool (no file context needed)



Scenario 7: General query (web search)

Q:
uv run main.py --query "What is Python isinstance function?"

Expected: Agent uses web_search tool or answers from knowledge



Scenario 8: Combine file + web search

Q:
uv run main.py --query "Is the API documentation following REST best practices?" --files test_files/api_documentation.txt

Expected: Agent reads file AND might search web for REST best practices



---------------  AI LLM ----------------


🏢 What is Groq?
Groq (the company) was NOT founded by Elon Musk. You might be confusing it with:

Grok (with a "k") - Elon Musk's AI chatbot from xAI
Groq (with a "q") - A different company that makes AI chips and provides LLM APIs
Groq Inc. was founded by Jonathan Ross (former Google engineer) and provides:

Fast AI inference hardware (LPU chips)
Cloud API for running LLMs (Llama, Mixtral, etc.)
🔄 How Your App Works Now
When USE_GROQ=true (Deployment):
python
llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=api_key
)
This means:

Your app sends requests to Groq's cloud API (groq.com)
Groq runs Meta's Llama 3.3 70B model on their servers
Results come back to your app
No Ollama involved - direct API call to Groq
When USE_GROQ=false (Local):
python
llm = ChatOllama(
    model="llama3.2"
)
This means:

Your app connects to Ollama running on your computer (localhost:11434)
Ollama runs Llama 3.2 locally on your machine
No Groq involved - completely local
📊 Comparison
Aspect	Groq (Cloud)	Ollama (Local)
Runs where?	Groq's servers	Your computer
Model	Llama 3.3 70B	Llama 3.2
Speed	Very fast	Medium
Cost	Free tier (limited)	Free (unlimited)
Internet needed?	Yes	No
Works on deployment?	✅ Yes	❌ No
🎯 Summary
Groq = Cloud API service (like OpenAI, but faster and cheaper)