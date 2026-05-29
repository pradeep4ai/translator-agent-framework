from __future__ import annotations

import logging
import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

from agents import TranslationPipeline, load_routing
from framework.llm import ClaudeProvider, LLMProvider, OpenAIProvider

log = logging.getLogger(__name__)

ROOT = Path(__file__).resolve().parent.parent
ROUTING_PATH = ROOT / "config" / "routing.yaml"


@lru_cache(maxsize=1)
def get_pipeline() -> TranslationPipeline:
    load_dotenv(ROOT / ".env")
    table = load_routing(ROUTING_PATH)

    providers: dict[str, LLMProvider] = {}

    if os.getenv("ANTHROPIC_API_KEY"):
        providers["claude"] = ClaudeProvider()
    else:
        log.warning("ANTHROPIC_API_KEY not set; Claude provider disabled")

    if os.getenv("OPENAI_API_KEY"):
        providers["openai"] = OpenAIProvider()
    else:
        log.warning("OPENAI_API_KEY not set; OpenAI provider disabled")

    # IndicTrans2 is opt-in via env flag to avoid loading torch unless needed.
    if os.getenv("ENABLE_INDICTRANS2", "0") == "1":
        from framework.llm import IndicTrans2Provider
        providers["indictrans2"] = IndicTrans2Provider()

    if "claude" not in providers:
        raise RuntimeError(
            "Claude provider is required as the quality judge. Set ANTHROPIC_API_KEY in .env."
        )

    return TranslationPipeline(table=table, providers=providers, judge=providers["claude"])


@lru_cache(maxsize=1)
def get_routing_table():
    return load_routing(ROUTING_PATH)
