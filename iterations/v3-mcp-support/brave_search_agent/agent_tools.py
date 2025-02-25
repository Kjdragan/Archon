import httpx
import asyncio
from typing import Dict, List, Any, Optional
import json
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Brave Search API endpoint - updated to correct endpoint
BRAVE_SEARCH_API_URL = "https://api.search.brave.com/res/v1/web/search"

async def fetch_search_results(
    api_key: str, 
    query: str, 
    count: int = 10, 
    offset: int = 0,
    country: str = "US",
    search_lang: str = "en",
    ui_lang: str = "en-US",
    safesearch: str = "moderate"
) -> Dict[str, Any]:
    """
    Fetch search results from the Brave Search API.
    
    Args:
        api_key: The Brave Search API key
        query: The search query
        count: Number of results to return (default: 10)
        offset: Offset for pagination (default: 0)
        country: Country code for localized results (default: US)
        search_lang: Language for search results (default: en)
        ui_lang: User interface language (default: en-US)
        safesearch: Content filtering level (off, moderate, strict) (default: moderate)
        
    Returns:
        A dictionary containing search results and metadata
    """
    try:
        headers = {
            "Accept": "application/json",
            "Accept-Encoding": "gzip",
            "X-Subscription-Token": api_key
        }
        
        params = {
            "q": query,
            "count": count,
            "offset": offset,
            "country": country,
            "search_lang": search_lang,
            "ui_lang": ui_lang,
            "safesearch": safesearch
        }
        
        # Log the request (without API key)
        logger.info(f"Searching for: {query} (count={count}, offset={offset})")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(
                BRAVE_SEARCH_API_URL,
                headers=headers,
                params=params
            )
            
            # Check if the request was successful
            if response.status_code == 200:
                return response.json()
            else:
                error_msg = f"Brave API error: {response.status_code} - {response.text}"
                logger.error(error_msg)
                return {"error": error_msg, "web": {"results": []}}
                
    except httpx.RequestError as e:
        error_msg = f"Request error: {str(e)}"
        logger.exception(error_msg)
        return {"error": error_msg, "web": {"results": []}}
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(error_msg)
        return {"error": error_msg, "web": {"results": []}}

async def fetch_page_content(api_key: str, url: str) -> str:
    """
    Fetch the content of a web page.
    
    Args:
        api_key: The Brave Search API key
        url: The URL of the page to fetch
        
    Returns:
        The content of the web page
    """
    try:
        headers = {
            "Accept": "text/html,application/xhtml+xml",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Log the request
        logger.info(f"Fetching content from: {url}")
        
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(url, headers=headers)
            
            # Check if the request was successful
            if response.status_code == 200:
                return response.text
            else:
                error_msg = f"Error fetching page: {response.status_code} - {response.text[:100]}"
                logger.error(error_msg)
                return ""
                
    except httpx.RequestError as e:
        error_msg = f"Request error: {str(e)}"
        logger.exception(error_msg)
        return ""
    except Exception as e:
        error_msg = f"Unexpected error: {str(e)}"
        logger.exception(error_msg)
        return ""

async def search_with_pagination(
    api_key: str, 
    query: str, 
    max_results: int = 30,
    country: str = "US",
    search_lang: str = "en",
    ui_lang: str = "en-US",
    safesearch: str = "moderate"
) -> Dict[str, Any]:
    """
    Search with pagination to get more results.
    
    Args:
        api_key: The Brave Search API key
        query: The search query
        max_results: Maximum number of results to return
        country: Country code for localized results (default: US)
        search_lang: Language for search results (default: en)
        ui_lang: User interface language (default: en-US)
        safesearch: Content filtering level (default: moderate)
        
    Returns:
        A dictionary containing combined search results
    """
    try:
        results_per_page = 10
        num_pages = (max_results + results_per_page - 1) // results_per_page
        
        all_results = {"web": {"results": []}}
        
        for page in range(num_pages):
            try:
                page_results = await fetch_search_results(
                    api_key, 
                    query, 
                    count=results_per_page, 
                    offset=page,
                    country=country,
                    search_lang=search_lang,
                    ui_lang=ui_lang,
                    safesearch=safesearch
                )
                
                # Check for errors
                if "error" in page_results:
                    logger.error(f"Error in page {page}: {page_results['error']}")
                    # If this is the first page and we got an error, return the error
                    if page == 0:
                        return page_results
                    # Otherwise, just break the loop and return what we have so far
                    break
                
                # Add results to the combined results
                if "web" in page_results and "results" in page_results["web"]:
                    all_results["web"]["results"].extend(page_results["web"]["results"])
                    
                    # Add metadata from the first page
                    if page == 0:
                        for key, value in page_results.items():
                            if key != "web":
                                all_results[key] = value
                                
                        # Copy web metadata
                        for key, value in page_results["web"].items():
                            if key != "results":
                                all_results["web"][key] = value
                
                # Break if we have enough results
                if len(all_results["web"]["results"]) >= max_results:
                    all_results["web"]["results"] = all_results["web"]["results"][:max_results]
                    break
                    
            except Exception as e:
                logger.exception(f"Error in pagination for page {page}: {str(e)}")
                # If this is the first page and we got an error, return an error
                if page == 0:
                    return {"error": f"Error in pagination: {str(e)}", "web": {"results": []}}
                # Otherwise, just break the loop and return what we have so far
                break
        
        return all_results
        
    except Exception as e:
        logger.exception(f"Error in search_with_pagination: {str(e)}")
        return {"error": f"Error in search_with_pagination: {str(e)}", "web": {"results": []}}
