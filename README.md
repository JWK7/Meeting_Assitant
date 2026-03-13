# Meeting Intelligence Assistant

AI-powered application that transforms meeting transcripts or recordings into structured insights and actionable outputs.

## Overview

This project demonstrates how modern LLM tools can be integrated into a backend service to process unstructured meeting content and generate summaries, decisions, action items, and high-level project plans. Built with Python, FastAPI, and the OpenAI API, it showcases practical patterns for developing AI-enabled applications.

### Key Concepts

- **LLM-powered summarization** and information extraction
- **Structured outputs** from language models
- **API-driven AI pipelines**
- **Processing unstructured text** into actionable insights

---

## Current Implementation Status

### Completed Features

- ✅ FastAPI application setup with `uv` package manager
- ✅ OpenAI API integration with Python SDK
- ✅ Environment-based configuration management
- ✅ Basic inference endpoint for LLM calls
- ✅ Request/response validation with Pydantic models
- ✅ Error handling and API validation

### In Progress

The full meeting intelligence features (transcript processing, summarization, action item extraction) are planned according to `PROJECT.md`.

---

## Prerequisites

- **Python**: 3.13.7 or higher
- **uv**: Package and project manager ([installation guide](https://github.com/astral-sh/uv))
- **OpenAI API Key**: Get one from [OpenAI Platform](https://platform.openai.com/api-keys)

---

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <repository-url>
cd Meeting_Assitant
```

### 2. Install Dependencies

The project uses `uv` for dependency management. Dependencies are automatically installed when you run the application.

```bash
# Verify uv is installed
uv --version

# Dependencies will be installed automatically when running the app
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your OpenAI API key:

```env
OPENAI_API_KEY=sk-proj-your-api-key-here
API_PORT=8000
LOG_LEVEL=INFO
MAX_TRANSCRIPT_LENGTH=50000
```

### 4. Verify Configuration

Run the configuration test to ensure your API key is working:

```bash
uv run python test_config.py
```

You should see output confirming the API key is loaded and a successful test call to OpenAI.

---

## Running the Application

### Start the Development Server

```bash
uv run python main.py
```

The server will start at `http://localhost:8000` with auto-reload enabled for development.

### Alternative: Run with uvicorn directly

```bash
uv run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Access the API Documentation

Once the server is running, visit:

- **Interactive API docs (Swagger UI)**: http://localhost:8000/docs
- **Alternative docs (ReDoc)**: http://localhost:8000/redoc
- **OpenAPI schema**: http://localhost:8000/openapi.json

---

## API Endpoints

### POST `/api/v1/inference`

Call OpenAI's inference endpoint with a custom prompt.

#### Request Body

```json
{
  "prompt": "Your prompt text here",
  "model": "gpt-4o-mini",
  "max_tokens": 1000,
  "temperature": 0.7
}
```

**Parameters:**

| Field | Type | Required | Default | Description |
|-------|------|----------|---------|-------------|
| `prompt` | string | Yes | - | The prompt to send to OpenAI |
| `model` | string | No | `gpt-4o-mini` | OpenAI model to use |
| `max_tokens` | integer | No | `1000` | Maximum tokens in response (1-4096) |
| `temperature` | float | No | `0.7` | Sampling temperature (0.0-2.0) |

#### Response

```json
{
  "response": "Generated text from the model",
  "model": "gpt-4o-mini-2024-07-18",
  "tokens_used": 42
}
```

**Fields:**

- `response`: The generated text from OpenAI
- `model`: The actual model version used
- `tokens_used`: Total tokens consumed (prompt + completion)

#### Example Usage

**Using curl:**

```bash
curl -X POST http://localhost:8000/api/v1/inference \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Explain FastAPI in one sentence",
    "model": "gpt-4o-mini",
    "max_tokens": 100,
    "temperature": 0.7
  }'
```

**Using Python:**

```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/inference",
    json={
        "prompt": "Write a haiku about coding",
        "model": "gpt-4o-mini",
        "max_tokens": 100,
        "temperature": 0.9
    }
)

print(response.json())
```

#### Error Responses

**Missing API Key (500):**
```json
{
  "detail": "OpenAI API key not configured. Please set OPENAI_API_KEY environment variable."
}
```

**OpenAI API Error (500):**
```json
{
  "detail": "OpenAI API error: <error message>"
}
```

**Validation Error (422):**
```json
{
  "detail": [
    {
      "loc": ["body", "prompt"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

---

## Project Structure

```
Meeting_Assitant/
├── src/
│   ├── api/              # API routes and endpoints
│   │   └── inference.py  # OpenAI inference endpoint
│   ├── config/           # Configuration management
│   │   └── settings.py   # Environment-based settings
│   ├── models/           # Data models and schemas
│   │   └── schemas.py    # Pydantic request/response models
│   ├── services/         # Business logic (planned)
│   ├── utils/            # Utility functions (planned)
│   └── main.py           # FastAPI application
├── main.py               # Application entry point
├── test_config.py        # API key verification test
├── test_settings.py      # Settings module test
├── .env                  # Environment variables (not in git)
├── .env.example          # Environment template
├── pyproject.toml        # Project dependencies
├── uv.lock              # Locked dependencies
├── PROJECT.md           # Detailed implementation plan
└── README.md            # This file
```

---

## Development

### Testing Configuration

Run the test scripts to verify your setup:

```bash
# Test OpenAI API key and connectivity
uv run python test_config.py

# Test settings module
uv run python test_settings.py
```

### Available Models

The endpoint supports any OpenAI chat model. Common options:

- `gpt-4o-mini` (default) - Fast and cost-effective
- `gpt-4o` - More capable, higher cost
- `gpt-4-turbo` - Balanced performance
- `gpt-3.5-turbo` - Fastest, lowest cost

### Code Quality

The project uses:

- **Pydantic** for data validation
- **Type hints** throughout the codebase
- **FastAPI** automatic API documentation

---

## Roadmap

See `PROJECT.md` for the complete implementation plan. Upcoming features include:

- Meeting transcript processing
- Automatic summarization
- Decision extraction
- Action item identification
- Project plan generation
- Persistent storage
- Background job processing
- Enhanced error handling and logging

---

## License

[Add your license here]

---

## Contributing

[Add contribution guidelines here]