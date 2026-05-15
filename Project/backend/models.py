from pydantic import BaseModel, Field


class CheckRequest(BaseModel):
    text: str = Field(..., min_length=10, description="Text to analyze")


class CheckResponse(BaseModel):
    probability: float = Field(..., ge=0.0, le=1.0)
