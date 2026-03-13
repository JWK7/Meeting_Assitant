# Meeting Intelligence Assistant - Implementation Plan

## Project Overview
AI-powered application that transforms meeting transcripts/recordings into structured insights including summaries, decisions, action items, and project plans. Built with Python, FastAPI, and OpenAI API.

---

## Phase 1: Project Foundation & Setup

### Task 1.1: Initialize Project Structure
- Create directory structure:
  ```
  /src
    /api          # API routes and endpoints
    /models       # Data models and schemas
    /services     # Business logic and LLM processing
    /utils        # Utility functions
    /config       # Configuration management
  /tests
    /unit
    /integration
  /examples       # Sample transcripts and outputs
  /docs          # Additional documentation
  ```
- Create `__init__.py` files for Python packages

### Task 1.2: Setup Dependency Management
- Create `requirements.txt` with:
  - fastapi
  - uvicorn[standard]
  - openai
  - pydantic
  - python-dotenv
  - pytest
  - httpx (for testing)
  - python-multipart (for file uploads)
- Create `requirements-dev.txt` for development dependencies:
  - black
  - flake8
  - mypy
  - pytest-cov

### Task 1.3: Configuration Management
- Create `.env.example` file with required environment variables:
  - OPENAI_API_KEY
  - API_PORT
  - LOG_LEVEL
  - MAX_TRANSCRIPT_LENGTH
- Create `src/config/settings.py` using pydantic BaseSettings for configuration management
- Add `.env` to `.gitignore`

### Task 1.4: Logging Setup
- Create `src/utils/logger.py` with structured logging configuration
- Setup log levels and formatting
- Configure log output destinations (console, file)

---

## Phase 2: Core Data Models

### Task 2.1: Define Domain Models
- Create `src/models/meeting.py`:
  - `MeetingMetadata` model (title, date, participants, duration)
  - `TranscriptInput` model (raw text or file)
  - `ProcessingStatus` enum (pending, processing, completed, failed)

### Task 2.2: Define Output Models
- Create `src/models/outputs.py`:
  - `MeetingSummary` model (executive summary, key points)
  - `Decision` model (decision text, context, owner)
  - `ActionItem` model (task, assignee, deadline, priority)
  - `ProjectPlan` model (goals, milestones, timeline)
  - `MeetingInsights` model (combines all outputs)

### Task 2.3: Define API Schemas
- Create `src/models/schemas.py`:
  - `TranscriptSubmissionRequest` schema
  - `TranscriptSubmissionResponse` schema (with job_id)
  - `ProcessingStatusResponse` schema
  - `MeetingInsightsResponse` schema
  - Error response schemas

---

## Phase 3: LLM Integration Layer

### Task 3.1: OpenAI Client Setup
- Create `src/services/llm_client.py`:
  - Initialize OpenAI client with API key
  - Configure default model (gpt-4-turbo or gpt-4)
  - Add retry logic and error handling
  - Add rate limiting considerations

### Task 3.2: Prompt Engineering
- Create `src/services/prompts.py`:
  - `SUMMARY_PROMPT`: Extract executive summary and key points
  - `DECISIONS_PROMPT`: Identify decisions made with context
  - `ACTION_ITEMS_PROMPT`: Extract action items with assignees and deadlines
  - `PROJECT_PLAN_PROMPT`: Generate high-level project plan from discussion
  - Include few-shot examples in prompts for better output quality

### Task 3.3: LLM Response Parser
- Create `src/services/response_parser.py`:
  - Parse LLM JSON responses into Pydantic models
  - Handle malformed responses with fallbacks
  - Validate structured outputs
  - Extract and clean data

### Task 3.4: Processing Service
- Create `src/services/meeting_processor.py`:
  - `MeetingProcessor` class with methods:
    - `process_transcript(transcript: str) -> MeetingInsights`
    - `generate_summary(transcript: str) -> MeetingSummary`
    - `extract_decisions(transcript: str) -> List[Decision]`
    - `extract_action_items(transcript: str) -> List[ActionItem]`
    - `generate_project_plan(transcript: str) -> ProjectPlan`
  - Orchestrate multiple LLM calls
  - Combine results into unified output

---

## Phase 4: FastAPI Application

### Task 4.1: Application Setup
- Create `src/main.py`:
  - Initialize FastAPI app with metadata
  - Configure CORS middleware
  - Add request logging middleware
  - Setup exception handlers

### Task 4.2: Health Check Endpoint
- Create `src/api/health.py`:
  - GET `/health` - Basic health check
  - GET `/health/ready` - Readiness check (includes OpenAI API connectivity)

### Task 4.3: Core API Endpoints
- Create `src/api/meetings.py`:
  - POST `/api/v1/meetings/process` - Submit transcript for processing
    - Accept text input or file upload
    - Return job_id for tracking
    - Start async processing
  - GET `/api/v1/meetings/{job_id}/status` - Check processing status
  - GET `/api/v1/meetings/{job_id}/insights` - Retrieve processed insights

### Task 4.4: Background Processing
- Create `src/services/job_manager.py`:
  - In-memory job queue (or use Redis for production)
  - Job status tracking
  - Background task execution
  - Result storage (in-memory or database)

---

## Phase 5: Input Handling & Validation

### Task 5.1: Transcript Ingestion
- Create `src/services/transcript_handler.py`:
  - Handle text input directly
  - Handle file uploads (.txt, .docx, .pdf)
  - Extract text from different file formats
  - Validate transcript length limits

### Task 5.2: Input Validation
- Add validation to API endpoints:
  - Check transcript not empty
  - Check transcript length within limits
  - Validate file types and sizes
  - Sanitize input text

### Task 5.3: Preprocessing
- Create `src/utils/text_processor.py`:
  - Clean and normalize transcript text
  - Remove excessive whitespace
  - Handle special characters
  - Chunk long transcripts if needed

---

## Phase 6: Error Handling & Resilience

### Task 6.1: Exception Handling
- Create `src/utils/exceptions.py`:
  - Custom exception classes:
    - `TranscriptTooLongError`
    - `LLMProcessingError`
    - `InvalidInputError`
    - `JobNotFoundError`
  - Exception handlers in FastAPI

### Task 6.2: Retry Logic
- Add retry mechanisms:
  - Retry LLM API calls on transient failures
  - Exponential backoff
  - Maximum retry limits
  - Proper error logging

### Task 6.3: Graceful Degradation
- Handle partial failures:
  - Return available insights if some processing steps fail
  - Provide error details in response
  - Log failures for debugging

---

## Phase 7: Testing

### Task 7.1: Unit Tests
- Create tests in `/tests/unit/`:
  - `test_models.py` - Test data models and validation
  - `test_prompt_engineering.py` - Test prompt generation
  - `test_response_parser.py` - Test LLM response parsing
  - `test_text_processor.py` - Test text preprocessing

### Task 7.2: Integration Tests
- Create tests in `/tests/integration/`:
  - `test_api_endpoints.py` - Test API endpoints with mock LLM
  - `test_meeting_processor.py` - Test end-to-end processing
  - `test_job_manager.py` - Test job lifecycle

### Task 7.3: Example Test Data
- Create `/examples/sample_transcripts/`:
  - `short_standup.txt` - Brief team standup
  - `product_planning.txt` - Product planning meeting
  - `technical_discussion.txt` - Technical architecture discussion
  - Expected outputs for each sample

### Task 7.4: LLM Integration Tests
- Create `/tests/integration/test_llm_live.py`:
  - Real OpenAI API tests (marked with pytest.mark.integration)
  - Use actual API calls with small examples
  - Verify output structure and quality

---

## Phase 8: Documentation

### Task 8.1: API Documentation
- Configure FastAPI automatic docs (Swagger/OpenAPI):
  - Add detailed docstrings to endpoints
  - Include request/response examples
  - Document error responses

### Task 8.2: Setup Guide
- Create `docs/SETUP.md`:
  - Prerequisites (Python version, OpenAI API key)
  - Installation steps
  - Environment configuration
  - Running the application

### Task 8.3: Usage Examples
- Create `docs/USAGE.md`:
  - API usage examples with curl/httpx
  - Sample requests and responses
  - Common use cases
  - Troubleshooting guide

### Task 8.4: Code Documentation
- Add comprehensive docstrings:
  - Module-level documentation
  - Class and method docstrings
  - Type hints throughout codebase

---

## Phase 9: Deployment Preparation

### Task 9.1: Docker Setup
- Create `Dockerfile`:
  - Multi-stage build for optimization
  - Python base image
  - Install dependencies
  - Copy application code
  - Expose API port
  - Set entrypoint

### Task 9.2: Docker Compose
- Create `docker-compose.yml`:
  - API service definition
  - Environment variable configuration
  - Volume mounts for development
  - Optional Redis service for job queue

### Task 9.3: Production Configuration
- Create `src/config/production.py`:
  - Production-safe defaults
  - Security headers
  - Rate limiting
  - CORS configuration

### Task 9.4: Deployment Documentation
- Create `docs/DEPLOYMENT.md`:
  - Docker deployment instructions
  - Environment variable reference
  - Scaling considerations
  - Monitoring recommendations

---

## Phase 10: Enhancement & Optimization

### Task 10.1: Performance Optimization
- Implement caching:
  - Cache repeated transcript processing
  - Cache LLM responses for identical inputs
- Optimize prompt sizes
- Batch processing capabilities

### Task 10.2: Additional Features (Optional)
- Persistent storage (PostgreSQL/MongoDB):
  - Store meeting history
  - User management
  - Search capabilities
- Real-time processing status with WebSockets
- Export formats (PDF, JSON, Markdown)
- Meeting comparison and analytics

### Task 10.3: Observability
- Add metrics:
  - Processing time tracking
  - API request metrics
  - LLM token usage tracking
- Application monitoring setup
- Cost tracking for OpenAI API usage

---

## Implementation Order Summary

1. **Phase 1-2** (Foundation): Setup project structure, dependencies, and data models
2. **Phase 3** (LLM Core): Build the LLM integration and processing logic
3. **Phase 4** (API): Create FastAPI application and endpoints
4. **Phase 5** (Input Handling): Implement transcript ingestion and validation
5. **Phase 6** (Resilience): Add error handling and retry logic
6. **Phase 7** (Testing): Comprehensive testing suite
7. **Phase 8** (Documentation): Complete documentation
8. **Phase 9** (Deployment): Containerization and deployment setup
9. **Phase 10** (Enhancement): Performance and additional features

---

## Key Dependencies Between Tasks

- Phase 2 must complete before Phase 3 (models needed for LLM integration)
- Phase 3 must complete before Phase 4 (processing logic needed for API)
- Phase 1-4 should complete before Phase 7 (need code to test)
- Phase 1-6 should complete before Phase 9 (need working app to containerize)

---

## Success Criteria

- API successfully processes meeting transcripts
- Returns structured outputs (summary, decisions, actions, plans)
- Handles errors gracefully
- Documented and tested
- Deployable via Docker
- Processing time < 30 seconds for typical transcripts
- Test coverage > 80%
