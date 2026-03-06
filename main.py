import os
import argparse
from pathlib import Path
from typing import List

import requests
from langchain_core.messages import HumanMessage, SystemMessage
from ddgs import DDGS
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langchain_ollama import ChatOllama
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()


@tool
def weather_api(city: str) -> str:
    """Get current weather data for a specific city using OpenWeatherMap API.

    Args:
        city: Name of the city (e.g., 'Delhi', 'New York', 'London')

    Returns:
        Current weather information including temperature, conditions, humidity, wind speed
    """
    api_key = os.getenv("OPENWEATHER_API_KEY")
    if not api_key:
        return "OpenWeatherMap API key not configured. Set OPENWEATHER_API_KEY in .env file."

    # First, get coordinates for the city using geocoding API
    geo_url = "http://api.openweathermap.org/geo/1.0/direct"
    geo_params = {"q": city, "limit": 1, "appid": api_key}

    """
    User: "Delhi weather"
    ↓
Call 1: Geocoding API
    Input: "Delhi"
    Output: lat=28.6139, lon=77.2090
    ↓
Call 2: Weather API
    Input: lat=28.6139, lon=77.2090
    Output: temp=31.43°C, humidity=17%, etc.
    """

    try:
        geo_resp = requests.get(geo_url, params=geo_params, timeout=10)
        geo_resp.raise_for_status()
        geo_data = geo_resp.json()

        if not geo_data:
            return f"City '{city}' not found. Please check the spelling."

        lat = geo_data[0]["lat"]
        lon = geo_data[0]["lon"]
        city_name = geo_data[0].get("name", city)
        country = geo_data[0].get("country", "")

    except (requests.RequestException, ValueError, KeyError) as exc:
        return f"Failed to get coordinates for {city}: {exc}"

    # Now get weather data using coordinates
    weather_url = "https://api.openweathermap.org/data/2.5/weather"
    weather_params = {
        "lat": lat,
        "lon": lon,
        "appid": api_key,
        "units": "metric",  # Use Celsius
    }

    try:
        weather_resp = requests.get(weather_url, params=weather_params, timeout=10)
        weather_resp.raise_for_status()
        data = weather_resp.json()

        # Extract relevant weather information
        temp = data["main"]["temp"]
        feels_like = data["main"]["feels_like"]
        humidity = data["main"]["humidity"]
        description = data["weather"][0]["description"]
        wind_speed = data["wind"]["speed"]

        result = f"""Weather in {city_name}, {country}:
- Temperature: {temp}°C (feels like {feels_like}°C)
- Conditions: {description.capitalize()}
- Humidity: {humidity}%
- Wind Speed: {wind_speed} m/s"""

        return result

    except (requests.RequestException, ValueError, KeyError) as exc:
        return f"Failed to get weather data for {city_name}: {exc}"


@tool
def web_search(query: str) -> str:
    """Search the web for up-to-date information and return concise results"""
    snippets: list[str] = []
    with DDGS() as ddgs:
        for item in ddgs.text(query, max_results=5):
            title = item.get("title", "")
            body = item.get("body", "")
            href = item.get("href", "")
            snippets.append(f" - {title}\n {body}\n Source:{href}")

    if not snippets:
        return "No relevant web results found"
    return "\n".join(snippets)


def build_agent():
    use_groq = os.getenv("USE_GROQ", "false").lower() == "true"

    if use_groq:
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY not set in environment")
        llm = ChatGroq(
            model="llama-3.3-70b-versatile", temperature=0.7, api_key=api_key
        )
    else:
        model_name = os.getenv("OLLAMA_MODEL", "llama3.2")
        llm = ChatOllama(model=model_name, temperature=0.7)

    tools = [weather_api, web_search]
    return create_react_agent(llm, tools)


def parse_args():
    parser = argparse.ArgumentParser(description="Agentic AI query runner")
    parser.add_argument(
        "--query", type=str, required=True, help="user query for the agent"
    )
    parser.add_argument(
        "--files",
        nargs="*",
        default=[],
        help="optional list of files to provide context to the agent",
    )
    return parser.parse_args()


def read_context_files(file_paths: List[str]) -> str:
    if not file_paths:
        return "No local files were provided"

    content_chunks: list[str] = []

    for raw_path in file_paths:
        path = Path(raw_path)
        if not path.exists() or not path.is_file():
            content_chunks.append(f"File {path} does not exist")
            continue

        try:
            file_text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            file_text = path.read_text(errors="ignore")
        except OSError as exc:
            content_chunks.append(f"## {raw_path}\n could not read file: {exc}")
            continue

        content_chunks.append(f"## {path}\n {file_text}")

    return "\n\n".join(content_chunks)


def main():
    load_dotenv()
    args = parse_args()

    file_content = read_context_files(args.files)
    agent = build_agent()

    system_instruction = (
        "You are an assistant that answers user queries using provided local files first. "
        "For weather queries, ALWAYS use the weather_api tool with the city name. "
        "For other information needs, use the web_search tool. "
        "Always provide a clear final answer and cite sources when tools are used. "
    )

    user_message = f"{system_instruction}\n\n user query: \n{args.query}\n\n local file context: \n{file_content}\n\nAnswer the query. use tools when necessary."

    result = agent.invoke({"messages": [("user", user_message)]})
    print("\nFinal response:\n")
    print(result["messages"][-1].content)


if __name__ == "__main__":
    main()
