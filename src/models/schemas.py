from pydantic import BaseModel, Field


class InferenceRequest(BaseModel):
    """Request model for OpenAI inference"""

    prompt: str = Field(..., description="The prompt to send to OpenAI", min_length=1)
    model: str = Field(default="gpt-4o-mini", description="The OpenAI model to use")
    max_tokens: int = Field(default=1000, description="Maximum tokens in response", gt=0, le=4096)
    temperature: float = Field(default=0.7, description="Sampling temperature", ge=0.0, le=2.0)


class InferenceResponse(BaseModel):
    """Response model for OpenAI inference"""

    response: str = Field(..., description="The generated response from OpenAI")
    model: str = Field(..., description="The model used for generation")
    tokens_used: int = Field(..., description="Total tokens used")
