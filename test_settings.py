#!/usr/bin/env python3
"""Test script to verify settings module reads environment variables correctly"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from src.config.settings import get_settings

def test_settings():
    """Test that settings module reads configuration correctly"""

    print("Testing Settings Module\n" + "="*50 + "\n")

    settings = get_settings()

    print(f"OpenAI API Key: {settings.openai_api_key[:10]}...{settings.openai_api_key[-4:]}")
    print(f"API Port: {settings.api_port}")
    print(f"Log Level: {settings.log_level}")
    print(f"Max Transcript Length: {settings.max_transcript_length}")

    # Verify API key is loaded
    if settings.openai_api_key and settings.openai_api_key.startswith("sk-"):
        print("\n✓ Settings module successfully loaded API key")
        return True
    else:
        print("\n❌ Settings module failed to load API key")
        return False


if __name__ == "__main__":
    success = test_settings()
    print("\n" + "="*50)
    print(f"Result: {'✓ Settings test passed' if success else '❌ Settings test failed'}")
