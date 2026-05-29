from __future__ import annotations

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agents import TranslationPipeline
from backend.deps import get_pipeline

router = APIRouter()


class TranslateRequest(BaseModel):
    source_lang: str = Field(..., examples=["hi"])
    target_lang: str = Field(..., examples=["en"])
    text: str = Field(..., min_length=1, max_length=4000)


class TranslateResponse(BaseModel):
    translation: str | None
    source_lang: str
    target_lang: str
    detected_lang: str | None
    detection_confidence: float | None
    lang_mismatch_warning: str | None
    provider_used: str | None
    model_used: str | None
    quality_score: int | None
    quality_notes: str | None
    attempts: int
    latency_ms: dict[str, float]
    errors: list[str]


@router.post("/translate", response_model=TranslateResponse)
def translate(
    body: TranslateRequest,
    pipeline: TranslationPipeline = Depends(get_pipeline),
) -> TranslateResponse:
    ctx = pipeline.run(body.source_lang, body.target_lang, body.text)
    if ctx.errors and ctx.output_text is None:
        raise HTTPException(status_code=400, detail={"errors": ctx.errors})
    return TranslateResponse(**ctx.to_response())
