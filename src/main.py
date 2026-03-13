from fastapi import FastAPI

from src.api.inference import router as inference_router

app = FastAPI(
    title="Meeting Intelligence Assistant",
    description="AI-powered application that transforms meeting transcripts into structured insights",
    version="0.1.0",
)

app.include_router(inference_router)
