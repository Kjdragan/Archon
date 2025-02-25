import asyncio
import os
import sys
import time
from dotenv import load_dotenv

# Add the parent directory to the Python path to make imports work
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import directly from the local modules
from agent import brave_search_agent, BraveSearchDeps
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def run_agent_with_retry(user_input, deps, message_history=None, max_retries=3):
    """
    Run the agent with retry logic.
    
    Args:
        user_input: The user's input
        deps: The agent dependencies
        message_history: The message history
        max_retries: Maximum number of retries
        
    Returns:
        The agent's response
    """
    if message_history is None:
        message_history = []
        
    retries = 0
    last_error = None
    
    while retries < max_retries:
        try:
            result = await brave_search_agent.run(
                user_input,
                deps=deps,
                message_history=message_history
            )
            return result, message_history
        except Exception as e:
            last_error = e
            logger.error(f"Error running agent (attempt {retries+1}/{max_retries}): {str(e)}")
            retries += 1
            if retries < max_retries:
                # Wait a bit before retrying
                await asyncio.sleep(1)
    
    # If we get here, all retries failed
    raise last_error

async def main():
    """
    Main function to run the Brave Search Agent.
    """
    # Load environment variables
    load_dotenv()
    
    # Get the Brave API key from environment variables
    brave_api_key = os.getenv("BRAVE_API_KEY")
    
    if not brave_api_key:
        print("Error: BRAVE_API_KEY environment variable not set.")
        print("Please set your Brave API key in the .env file.")
        return
    
    # Create dependencies
    deps = BraveSearchDeps(brave_api_key=brave_api_key)
    
    # Welcome message
    print("Welcome to the Brave Search Agent!")
    print("Type 'exit' to quit.")
    print()
    
    # Main conversation loop
    message_history = []
    
    while True:
        # Get user input
        user_input = input("You: ")
        
        # Check if user wants to exit
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break
        
        try:
            # Run the agent with retry logic
            result, message_history = await run_agent_with_retry(
                user_input,
                deps=deps,
                message_history=message_history
            )
            
            # Print the agent's response
            print("\nAgent:", result.data)
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print("Sorry, I encountered an error. Please try again with a different query.")

if __name__ == "__main__":
    asyncio.run(main())
