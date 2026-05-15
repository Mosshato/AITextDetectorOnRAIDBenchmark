from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware

from models import CheckRequest, CheckResponse
from services.detector import callModel

app = FastAPI(title="AI Text Detector API", version="1.0.0")

# Allow frontend (localhost:3000) to call the backend during development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/check", response_model=CheckResponse)
def check_text(payload: CheckRequest) -> CheckResponse:
    text = payload.text.strip()

    if not text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Text must not be empty.",
        )

    if len(text) < 10:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Text is too short. Please provide at least 10 characters.",
        )

    probability = callModel(text)
    return CheckResponse(probability=probability)
