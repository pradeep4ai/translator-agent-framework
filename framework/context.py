from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Context:
    source_lang: str
    target_lang: str
    input_text: str

    detected_lang: str | None = None
    detection_confidence: float | None = None
    lang_mismatch_warning: str | None = None

    chosen_provider: str | None = None
    chosen_model: str | None = None

    output_text: str | None = None
    quality_score: int | None = None
    quality_notes: str | None = None

    attempts: int = 0
    errors: list[str] = field(default_factory=list)
    latency_ms: dict[str, float] = field(default_factory=dict)
    extras: dict[str, Any] = field(default_factory=dict)

    def fail(self, msg: str) -> None:
        self.errors.append(msg)

    def to_response(self) -> dict[str, Any]:
        return {
            "translation": self.output_text,
            "source_lang": self.source_lang,
            "target_lang": self.target_lang,
            "detected_lang": self.detected_lang,
            "detection_confidence": self.detection_confidence,
            "lang_mismatch_warning": self.lang_mismatch_warning,
            "provider_used": self.chosen_provider,
            "model_used": self.chosen_model,
            "quality_score": self.quality_score,
            "quality_notes": self.quality_notes,
            "attempts": self.attempts,
            "latency_ms": self.latency_ms,
            "errors": self.errors,
        }
