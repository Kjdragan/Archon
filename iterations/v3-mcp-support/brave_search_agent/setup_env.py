#!/usr/bin/env python3
"""
Setup script to create a .env file for the Brave Search Agent.
"""

import os
import sys

def setup_env():
    """Create a .env file with the necessary environment variables."""
    env_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
    
    # Check if .env file already exists
    if os.path.exists(env_file):
        overwrite = input("A .env file already exists. Overwrite? (y/n): ")
        if overwrite.lower() != 'y':
            print("Setup cancelled.")
            return
    
    # Get API keys from user
    openai_api_key = input("Enter your OpenAI API key: ")
    brave_api_key = input("Enter your Brave Search API key: ")
    model_name = input("Enter the model name (default: gpt-4o-mini): ") or "gpt-4o-mini"
    
    # Create .env file
    with open(env_file, 'w') as f:
        f.write(f"# OpenAI API Key\n")
        f.write(f"OPENAI_API_KEY={openai_api_key}\n\n")
        f.write(f"# Brave Search API Key\n")
        f.write(f"BRAVE_API_KEY={brave_api_key}\n\n")
        f.write(f"# Model name\n")
        f.write(f"MODEL_NAME={model_name}\n")
    
    print(f".env file created at {env_file}")
    print("You can now run the agent with 'python main.py'")

if __name__ == "__main__":
    setup_env()
