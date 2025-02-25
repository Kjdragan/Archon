#!/usr/bin/env python3
"""
Run script for the Brave Search Agent.
This script checks for the .env file and runs the setup if needed,
then runs the main agent.
"""

import os
import sys
import asyncio
from dotenv import load_dotenv

def check_env():
    """Check if the .env file exists and has the necessary variables."""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    if not os.path.exists(env_file):
        print("No .env file found. Running setup...")
        from setup_env import setup_env
        setup_env()
        return False
    
    # Load environment variables
    load_dotenv(env_file)
    
    # Check for required variables
    if not os.getenv('OPENAI_API_KEY'):
        print("OPENAI_API_KEY not found in .env file.")
        return False
    
    if not os.getenv('BRAVE_API_KEY'):
        print("BRAVE_API_KEY not found in .env file.")
        return False
    
    return True

async def run_agent():
    """Run the Brave Search Agent."""
    from main import main
    await main()

if __name__ == "__main__":
    if check_env():
        asyncio.run(run_agent())
