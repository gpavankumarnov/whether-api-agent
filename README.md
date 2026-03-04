# Weather API Agent

An intelligent AI agent that answers queries using local Ollama models and can fetch real-time weather data via OpenWeatherMap API or search the web using DuckDuckGo.

## Features

- **Local AI Model**: Runs on Ollama (llama3.2) - no cloud API costs
- **Real-time Weather**: Fetches current weather for any city worldwide
- **Web Search**: Falls back to DuckDuckGo search for general queries
- **File Context**: Can read and analyze local files you provide
- **ReAct Agent**: Autonomously decides which tool to use based on your query

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
bash
uv run main.py --query "What are the main topics covered in this file?" --files test_files/python_basics.txt
Expected: Agent summarizes Python basics (variables, functions, loops, etc.)



Scenario 2: Compare weather data with real-time API
bash
uv run main.py --query "Compare the Delhi temperature in the file with current weather" --files test_files/weather_data.txt
Expected: Agent reads file data AND calls weather_api("Delhi") to compare




Scenario 3: Code explanation
bash
uv run main.py --query "Explain what this code does and how it works" --files test_files/code_snippet.py
Expected: Agent analyzes the WeatherAnalyzer class and explains its methods



Scenario 4: Multiple files
bash
uv run main.py --query "What's the relationship between these files?" --files test_files/python_basics.txt test_files/code_snippet.py
Expected: Agent reads both files and explains how the code uses Python concepts



Scenario 5: Extract specific info
bash
uv run main.py --query "What are the error codes in the API documentation?" --files test_files/api_documentation.txt
Expected: Agent extracts and lists error codes (400, 401, 404, 500)



Scenario 6: Weather query without file (baseline)
bash
uv run main.py --query "What's the weather in Mumbai today?"
Expected: Agent uses weather_api tool (no file context needed)



Scenario 7: General query (web search)
bash
uv run main.py --query "What is Python isinstance function?"
Expected: Agent uses web_search tool or answers from knowledge



Scenario 8: Combine file + web search
bash
uv run main.py --query "Is the API documentation following REST best practices?" --files test_files/api_documentation.txt
Expected: Agent reads file AND might search web for REST best practices

