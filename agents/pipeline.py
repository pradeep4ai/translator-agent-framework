from __future__ import annotations

import logging

from framework.context import Context
from framework.llm import LLMProvider

from agents.detector import LanguageDetectorAgent
from agents.reviewer import QualityReviewerAgent
from agents.router import RouterAgent, RoutingTable
from agents.translator import TranslatorAgent

log = logging.getLogger(__name__)


class TranslationPipeline:
    """Custom orchestrator that handles detect -> route -> translate -> review,
    with a quality-driven retry loop that escalates to a stronger provider."""

    def __init__(
        self,
        table: RoutingTable,
        providers: dict[str, LLMProvider],
        judge: LLMProvider,
        judge_model: str | None = None,
    ) -> None:
        self.table = table
        self.detector = LanguageDetectorAgent()
        self.router = RouterAgent(table)
        self.translator = TranslatorAgent(providers)
        self.reviewer = QualityReviewerAgent(judge, judge_model)

    def run(self, source_lang: str, target_lang: str, text: str) -> Context:
        ctx = Context(source_lang=source_lang, target_lang=target_lang, input_text=text)

        ctx = self.detector(ctx)
        if ctx.errors:
            return ctx

        for _ in range(self.table.max_attempts):
            ctx = self.router(ctx)
            if ctx.errors:
                return ctx
            ctx = self.translator(ctx)
            if ctx.errors:
                return ctx
            ctx = self.reviewer(ctx)
            if ctx.errors:
                return ctx
            if (ctx.quality_score or 0) >= self.table.min_quality:
                return ctx
            log.info(
                "quality %s below %s, retrying with stronger model",
                ctx.quality_score, self.table.min_quality,
            )
        return ctx
