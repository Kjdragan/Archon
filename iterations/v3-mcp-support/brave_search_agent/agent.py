from pydantic_ai import Agent, RunContext
from pydantic_ai.models.openai import OpenAIModel
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
import os
import logging
from dotenv import load_dotenv

# Import tools and prompts using direct imports
from agent_tools import fetch_search_results, fetch_page_content
from agent_prompts import SYSTEM_PROMPT

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Get API key and model from environment
api_key = os.getenv('OPENAI_API_KEY')
model_name = os.getenv('MODEL_NAME', 'gpt-4o-mini')

@dataclass
class BraveSearchDeps:
    """Dependencies for the Brave Search agent."""
    brave_api_key: str

# Initialize the OpenAI model
model = OpenAIModel(model_name, api_key=api_key)

# Create the agent
brave_search_agent = Agent(
    model,
    system_prompt=SYSTEM_PROMPT,
    deps_type=BraveSearchDeps
)

@brave_search_agent.tool
async def search_web(ctx: RunContext[BraveSearchDeps], query: str, count: int = 10) -> Dict[str, Any]:
    """
    Search the web using the Brave API.
    
    Args:
        ctx: The context including the Brave API key
        query: The search query
        count: Number of results to return (default: 10)
        
    Returns:
        A dictionary containing search results and metadata
    """
    try:
        brave_api_key = ctx.deps.brave_api_key
        search_results = await fetch_search_results(brave_api_key, query, count)
        
        # Check if the result contains an error
        if "error" in search_results:
            logger.error(f"Brave API error: {search_results['error']}")
            return {"error": search_results["error"], "web": {"results": []}}
            
        return search_results
    except Exception as e:
        logger.exception(f"Error in search_web: {str(e)}")
        return {"error": str(e), "web": {"results": []}}

@brave_search_agent.tool
async def get_page_content(ctx: RunContext[BraveSearchDeps], url: str) -> str:
    """
    Fetch the content of a web page.
    
    Args:
        ctx: The context including the Brave API key
        url: The URL of the page to fetch
        
    Returns:
        The content of the web page
    """
    try:
        brave_api_key = ctx.deps.brave_api_key
        content = await fetch_page_content(brave_api_key, url)
        
        # Check if the result contains an error
        if "error" in content:
            logger.error(f"Brave API error: {content['error']}")
            return ""
            
        return content
    except Exception as e:
        logger.exception(f"Error in get_page_content: {str(e)}")
        return ""

@brave_search_agent.tool
async def summarize_search_results(ctx: RunContext[BraveSearchDeps], results: Dict[str, Any]) -> str:
    """
    Summarize the search results in a human-readable format.
    
    Args:
        ctx: The context
        results: The search results to summarize
        
    Returns:
        A human-readable summary of the search results
    """
    try:
        if not results or not results.get('web', {}).get('results'):
            return "No search results found."
        
        web_results = results['web']['results']
        summary = "## Search Results\n\n"
        
        for i, result in enumerate(web_results, 1):
            title = result.get('title', 'No title')
            url = result.get('url', 'No URL')
            description = result.get('description', 'No description')
            
            summary += f"### {i}. {title}\n"
            summary += f"**URL**: {url}\n"
            summary += f"**Description**: {description}\n\n"
        
        return summary
    except Exception as e:
        logger.exception(f"Error in summarize_search_results: {str(e)}")
        return ""
