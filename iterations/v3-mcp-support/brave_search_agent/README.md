# Brave Search Agent

An AI agent that can search the web using the Brave API.

## Setup

1. Create a `.env` file in the `brave_search_agent` directory with the following variables:

```
# OpenAI API Key - Required for the language model
OPENAI_API_KEY=your_openai_api_key_here

# Brave Search API Key - Required for web search functionality
# Sign up at https://brave.com/search/api/
BRAVE_API_KEY=your_brave_api_key_here

# Model name - Optional, defaults to gpt-4o-mini
MODEL_NAME=gpt-4o-mini
```

2. Install the required dependencies:

```bash
pip install pydantic-ai httpx python-dotenv
```

## Usage

Run the main script to start the agent:

```bash
cd brave_search_agent
python main.py
```

## Features

- Search the web using the Brave Search API
- Fetch the content of web pages
- Summarize search results in a human-readable format
- Handle pagination for large result sets

## API Parameters

The Brave Search API supports the following parameters:

- `query`: The search query
- `count`: Number of results to return (default: 10)
- `offset`: Offset for pagination (default: 0)
- `country`: Country code for localized results (default: US)
- `search_lang`: Language for search results (default: en)
- `ui_lang`: User interface language (default: en-US)
- `safesearch`: Content filtering level (off, moderate, strict) (default: moderate)

## Examples

Here are some example queries you can try:

- "What is the latest news about AI?"
- "Find information about climate change"
- "Search for Python programming tutorials"
- "Look up the history of the internet"
