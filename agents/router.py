from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import yaml

from framework.agent import BaseAgent
from framework.context import Context


@dataclass
class Rule:
    source: str
    target: str
    provider: str
    model: str
    strong_provider: str
    strong_model: str

    def matches(self, src: str, tgt: str) -> bool:
        return (self.source in ("*", src)) and (self.target in ("*", tgt))


@dataclass
class Language:
    code: str
    name: str
    script: str


@dataclass
class RoutingTable:
    rules: list[Rule]
    indian: list[Language]
    western: list[Language]
    min_quality: int
    max_attempts: int

    def all_codes(self) -> set[str]:
        return {lang.code for lang in (*self.indian, *self.western)}

    def all_languages(self) -> list[Language]:
        return [*self.indian, *self.western]

    def resolve(self, source: str, target: str) -> Rule:
        for rule in self.rules:
            if rule.matches(source, target):
                return rule
        raise ValueError(f"No routing rule for {source} -> {target}")


def load_routing(path: str | Path) -> RoutingTable:
    data = yaml.safe_load(Path(path).read_text(encoding="utf-8"))
    rules = [Rule(**r) for r in data["rules"]]
    indian = [Language(**l) for l in data["languages"]["indian"]]
    western = [Language(**l) for l in data["languages"]["western"]]
    retry = data.get("retry", {})
    return RoutingTable(
        rules=rules,
        indian=indian,
        western=western,
        min_quality=int(retry.get("min_acceptable_quality", 3)),
        max_attempts=int(retry.get("max_attempts", 2)),
    )


class RouterAgent(BaseAgent):
    name = "router"

    def __init__(self, table: RoutingTable) -> None:
        self.table = table

    def run(self, ctx: Context) -> Context:
        codes = self.table.all_codes()
        if ctx.source_lang not in codes:
            ctx.fail(f"unsupported source language: {ctx.source_lang}")
            return ctx
        if ctx.target_lang not in codes:
            ctx.fail(f"unsupported target language: {ctx.target_lang}")
            return ctx
        if ctx.source_lang == ctx.target_lang:
            ctx.fail("source and target languages must differ")
            return ctx

        rule = self.table.resolve(ctx.source_lang, ctx.target_lang)
        # On a retry attempt, escalate to the strong provider/model.
        if ctx.attempts >= 1:
            ctx.chosen_provider = rule.strong_provider
            ctx.chosen_model = rule.strong_model
        else:
            ctx.chosen_provider = rule.provider
            ctx.chosen_model = rule.model
        return ctx
