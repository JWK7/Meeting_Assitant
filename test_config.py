#!/usr/bin/env python3
"""Test script to verify OpenAI API key configuration"""

import os
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

def test_api_key():
    """Verify API key is loaded and can initialize OpenAI client"""

    # Check if API key is loaded
    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("❌ OPENAI_API_KEY not found in environment")
        return False

    # Check if key has expected format
    if not api_key.startswith("sk-"):
        print("❌ API key doesn't appear to be valid (should start with 'sk-')")
        return False

    print(f"✓ API key found: {api_key[:10]}...{api_key[-4:]}")

    # Try to initialize OpenAI client
    try:
        client = OpenAI(api_key=api_key)
        print("✓ OpenAI client initialized successfully")

        # Try a simple API call
        print("\nTesting API connection with a simple request...")
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": "Say 'Hello'"}],
            max_tokens=10,
        )

        print(f"✓ API call successful!")
        print(f"  Model: {response.model}")
        print(f"  Response: {response.choices[0].message.content}")
        print(f"  Tokens used: {response.usage.total_tokens}")

        return True

    except Exception as e:
        print(f"❌ Error initializing OpenAI client or making API call: {e}")
        return False


if __name__ == "__main__":
    print("Testing OpenAI API Key Configuration\n" + "="*50 + "\n")
    success = test_api_key()
    print("\n" + "="*50)
    print(f"Result: {'✓ All tests passed' if success else '❌ Tests failed'}")
