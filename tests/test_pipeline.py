from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from agents import TranslationPipeline, load_routing
from framework.llm import LLMResponse

ROUTING = Path(__file__).resolve().parent.parent / "config" / "routing.yaml"


@dataclass
class FakeProvider:
    name: str
    default_model: str = "fake-model-1"
    canned_text: str = "Hello, how are you?"
    canned_score: int = 5

    def complete(self, prompt, *, system=None, model=None, temperature=0.2, max_tokens=1024):
        # The reviewer asks for JSON, distinguish by system content / prompt structure.
        if "quality reviewer" in (system or "").lower() or '"score"' in prompt:
            return LLMResponse(
                text=f'{{"score": {self.canned_score}, "notes": "ok"}}',
                model=model or self.default_model,
                provider=self.name,
            )
        return LLMResponse(text=self.canned_text, model=model or self.default_model, provider=self.name)


def test_pipeline_happy_path():
    table = load_routing(ROUTING)
    claude = FakeProvider(name="claude", default_model="claude-sonnet-4-6", canned_text="Hello")
    openai = FakeProvider(name="openai", default_model="gpt-4o", canned_text="Hello")
    pipeline = TranslationPipeline(
        table=table,
        providers={"claude": claude, "openai": openai},
        judge=claude,
    )
    ctx = pipeline.run("hi", "en", "नमस्ते")
    assert ctx.errors == []
    assert ctx.output_text == "Hello"
    assert ctx.chosen_provider == "claude"
    assert ctx.quality_score == 5
    assert ctx.attempts == 1


def test_pipeline_retries_on_low_quality():
    table = load_routing(ROUTING)
    # Judge returns score=2 to trigger a retry.
    weak_judge = FakeProvider(name="claude", canned_score=2)
    claude = FakeProvider(name="claude", default_model="claude-sonnet-4-6")
    openai = FakeProvider(name="openai", default_model="gpt-4o")
    pipeline = TranslationPipeline(
        table=table,
        providers={"claude": claude, "openai": openai},
        judge=weak_judge,
    )
    ctx = pipeline.run("hi", "en", "test")
    # Two attempts, second one used the strong (openai) provider per routing rule.
    assert ctx.attempts == 2
    assert ctx.chosen_provider == "openai"


def test_pipeline_detects_script_mismatch():
    table = load_routing(ROUTING)
    claude = FakeProvider(name="claude")
    openai = FakeProvider(name="openai")
    pipeline = TranslationPipeline(
        table=table,
        providers={"claude": claude, "openai": openai},
        judge=claude,
    )
    # Claim source is Telugu but pass Devanagari (Hindi) text.
    ctx = pipeline.run("te", "en", "नमस्ते आप कैसे हैं")
    assert ctx.lang_mismatch_warning is not None
    assert "DEVANAGARI" in ctx.lang_mismatch_warning
