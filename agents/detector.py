from __future__ import annotations

import unicodedata

from framework.agent import BaseAgent
from framework.context import Context


# Quick script-based detection. Coarse but free and instant.
# Distinguishes Devanagari-family languages (hi/mr/bho/ne) only by user-supplied hint;
# disambiguation between them requires an LLM call (expensive) and is out of MVP scope.
SCRIPT_HINTS: dict[str, set[str]] = {
    "te": {"TELUGU"},
    "gu": {"GUJARATI"},
    "kn": {"KANNADA"},
    "hi": {"DEVANAGARI"},
    "mr": {"DEVANAGARI"},
    "bho": {"DEVANAGARI"},
    "ne": {"DEVANAGARI"},
    "en": {"LATIN"},
    "de": {"LATIN"},
    "fr": {"LATIN"},
}


def _dominant_script(text: str) -> str | None:
    counts: dict[str, int] = {}
    for ch in text:
        if not ch.isalpha():
            continue
        try:
            block = unicodedata.name(ch).split()[0]
        except ValueError:
            continue
        counts[block] = counts.get(block, 0) + 1
    if not counts:
        return None
    return max(counts, key=counts.get)


class LanguageDetectorAgent(BaseAgent):
    name = "detector"

    def run(self, ctx: Context) -> Context:
        dominant = _dominant_script(ctx.input_text)
        ctx.detected_lang = ctx.source_lang  # default: trust user
        if dominant is None:
            return ctx

        expected = SCRIPT_HINTS.get(ctx.source_lang, set())
        if expected and dominant not in expected:
            ctx.lang_mismatch_warning = (
                f"Input script looks like {dominant}, but source language was set to "
                f"{ctx.source_lang} (expected script: {', '.join(expected)})."
            )
            ctx.detection_confidence = 0.4
        else:
            ctx.detection_confidence = 0.9
        return ctx
