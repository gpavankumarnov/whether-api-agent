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
