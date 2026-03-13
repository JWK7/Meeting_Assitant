from fastapi import APIRouter, HTTPException, Depends
from openai import OpenAI, OpenAIError

from src.config.settings import Settings, get_settings
from src.models.schemas import InferenceRequest, InferenceResponse

router = APIRouter(prefix="/api/v1", tags=["inference"])


def get_openai_client(settings: Settings = Depends(get_settings)) -> OpenAI:
    """Get OpenAI client instance"""
    if not settings.openai_api_key:
        raise HTTPException(
            status_code=500,
            detail="OpenAI API key not configured. Please set OPENAI_API_KEY environment variable.",
        )
    return OpenAI(api_key=settings.openai_api_key)


@router.post("/inference", response_model=InferenceResponse)
async def create_inference(
    request: InferenceRequest,
    client: OpenAI = Depends(get_openai_client),
) -> InferenceResponse:
    """
    Call OpenAI's inference endpoint with the provided prompt.

    Args:
        request: The inference request containing the prompt and parameters
        client: The OpenAI client instance

    Returns:
        InferenceResponse with the generated text and metadata
    """
    try:
        completion = client.chat.completions.create(
            model=request.model,
            messages=[
                {"role": "user", "content": request.prompt}
            ],
            max_tokens=request.max_tokens,
            temperature=request.temperature,
        )

        response_text = completion.choices[0].message.content or ""
        tokens_used = completion.usage.total_tokens if completion.usage else 0

        return InferenceResponse(
            response=response_text,
            model=completion.model,
            tokens_used=tokens_used,
        )

    except OpenAIError as e:
        raise HTTPException(
            status_code=500,
            detail=f"OpenAI API error: {str(e)}",
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Unexpected error: {str(e)}",
        )
