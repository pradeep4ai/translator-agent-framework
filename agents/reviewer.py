from __future__ import annotations

import json
import os
import re

from framework.agent import BaseAgent
from framework.context import Context
from framework.llm import LLMProvider

from agents.translator import LANG_NAMES


REVIEW_PROMPT = """You are a translation quality reviewer.

Source ({source_name}):
{source_text}

Translation ({target_name}):
{translation}

Score the translation on a 1-5 integer scale (5 = perfect, 1 = unusable).
Consider: meaning preservation, fluency, grammar, register.

Respond with strict JSON only, no markdown, no prose:
{{"score": <int 1-5>, "notes": "<one short sentence>"}}"""


class QualityReviewerAgent(BaseAgent):
    name = "reviewer"

    def __init__(self, judge: LLMProvider, judge_model: str | None = None) -> None:
        self.judge = judge
        self.judge_model = judge_model or os.getenv("CLAUDE_MODEL_FAST", "claude-haiku-4-5-20251001")

    def run(self, ctx: Context) -> Context:
        if not ctx.output_text:
            ctx.fail("reviewer: no translation to score")
            return ctx

        prompt = REVIEW_PROMPT.format(
            source_name=LANG_NAMES.get(ctx.source_lang, ctx.source_lang),
            target_name=LANG_NAMES.get(ctx.target_lang, ctx.target_lang),
            source_text=ctx.input_text,
            translation=ctx.output_text,
        )
        response = self.judge.complete(
            prompt,
            system="You are a terse, honest translation quality judge. Reply with JSON only.",
            model=self.judge_model,
            temperature=0.0,
            max_tokens=200,
        )
        score, notes = _parse_score(response.text)
        ctx.quality_score = score
        ctx.quality_notes = notes
        return ctx


def _parse_score(text: str) -> tuple[int, str]:
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if not match:
        return 3, f"could not parse judge output: {text[:120]}"
    try:
        data = json.loads(match.group(0))
        return int(data.get("score", 3)), str(data.get("notes", ""))
    except (json.JSONDecodeError, ValueError, TypeError):
        return 3, f"could not parse judge output: {text[:120]}"
