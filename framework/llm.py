from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol, runtime_checkable


@dataclass
class LLMResponse:
    text: str
    model: str
    provider: str
    usage: dict | None = None


@runtime_checkable
class LLMProvider(Protocol):
    name: str
    default_model: str

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> LLMResponse: ...


class ClaudeProvider:
    name = "claude"

    def __init__(self, api_key: str | None = None, default_model: str | None = None) -> None:
        import anthropic

        self._client = anthropic.Anthropic(api_key=api_key or os.getenv("ANTHROPIC_API_KEY"))
        self.default_model = default_model or os.getenv("CLAUDE_MODEL_STRONG", "claude-sonnet-4-6")

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        used_model = model or self.default_model
        resp = self._client.messages.create(
            model=used_model,
            max_tokens=max_tokens,
            temperature=temperature,
            system=system or "You are a precise multilingual translator.",
            messages=[{"role": "user", "content": prompt}],
        )
        text = "".join(block.text for block in resp.content if getattr(block, "type", None) == "text")
        return LLMResponse(
            text=text.strip(),
            model=used_model,
            provider=self.name,
            usage={"input_tokens": resp.usage.input_tokens, "output_tokens": resp.usage.output_tokens},
        )


class OpenAIProvider:
    name = "openai"

    def __init__(self, api_key: str | None = None, default_model: str | None = None) -> None:
        import openai

        self._client = openai.OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
        self.default_model = default_model or os.getenv("OPENAI_MODEL", "gpt-4o")

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float = 0.2,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        used_model = model or self.default_model
        resp = self._client.chat.completions.create(
            model=used_model,
            temperature=temperature,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system or "You are a precise multilingual translator."},
                {"role": "user", "content": prompt},
            ],
        )
        choice = resp.choices[0]
        return LLMResponse(
            text=(choice.message.content or "").strip(),
            model=used_model,
            provider=self.name,
            usage={
                "input_tokens": resp.usage.prompt_tokens if resp.usage else None,
                "output_tokens": resp.usage.completion_tokens if resp.usage else None,
            },
        )


class IndicTrans2Provider:
    """Wrapper for AI4Bharat IndicTrans2. Lazy-loads transformers/torch only when first used."""

    name = "indictrans2"
    default_model = "ai4bharat/indictrans2-indic-en-1B"

    def __init__(self, model_id: str | None = None) -> None:
        self.default_model = model_id or self.default_model
        self._tokenizer = None
        self._model = None
        self._processor = None

    def _ensure_loaded(self) -> None:
        if self._model is not None:
            return
        try:
            from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        except ImportError as exc:
            raise RuntimeError(
                "IndicTrans2Provider requires `transformers` and `torch`. "
                "Install with: pip install -r requirements-indictrans.txt"
            ) from exc
        self._tokenizer = AutoTokenizer.from_pretrained(self.default_model, trust_remote_code=True)
        self._model = AutoModelForSeq2SeqLM.from_pretrained(self.default_model, trust_remote_code=True)

    def complete(
        self,
        prompt: str,
        *,
        system: str | None = None,
        model: str | None = None,
        temperature: float = 0.0,
        max_tokens: int = 1024,
    ) -> LLMResponse:
        self._ensure_loaded()
        assert self._tokenizer is not None and self._model is not None
        inputs = self._tokenizer(prompt, return_tensors="pt", truncation=True)
        outputs = self._model.generate(**inputs, max_length=max_tokens, num_beams=5, early_stopping=True)
        text = self._tokenizer.decode(outputs[0], skip_special_tokens=True)
        return LLMResponse(text=text.strip(), model=self.default_model, provider=self.name)
