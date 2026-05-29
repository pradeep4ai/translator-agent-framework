from __future__ import annotations

from pathlib import Path

import pytest

from agents.router import RouterAgent, load_routing
from framework.context import Context

ROUTING = Path(__file__).resolve().parent.parent / "config" / "routing.yaml"


@pytest.fixture(scope="module")
def table():
    return load_routing(ROUTING)


@pytest.mark.parametrize(
    "src,tgt,expected_provider",
    [
        ("hi", "en", "claude"),
        ("hi", "de", "claude"),
        ("hi", "fr", "claude"),
        ("te", "en", "claude"),
        ("mr", "fr", "claude"),
        ("gu", "de", "claude"),
        ("kn", "en", "claude"),
        ("bho", "en", "claude"),
        ("en", "bho", "claude"),
        ("ne", "en", "claude"),
        ("en", "ne", "claude"),
        ("en", "hi", "claude"),
        ("de", "te", "claude"),
    ],
)
def test_every_pair_routes(table, src, tgt, expected_provider):
    agent = RouterAgent(table)
    ctx = Context(source_lang=src, target_lang=tgt, input_text="hello")
    ctx = agent.run(ctx)
    assert ctx.errors == []
    assert ctx.chosen_provider == expected_provider
    assert ctx.chosen_model


def test_unsupported_source(table):
    agent = RouterAgent(table)
    ctx = Context(source_lang="xx", target_lang="en", input_text="hi")
    ctx = agent.run(ctx)
    assert ctx.errors


def test_same_source_target(table):
    agent = RouterAgent(table)
    ctx = Context(source_lang="hi", target_lang="hi", input_text="hi")
    ctx = agent.run(ctx)
    assert ctx.errors


def test_retry_escalates(table):
    agent = RouterAgent(table)
    ctx = Context(source_lang="hi", target_lang="en", input_text="hi")
    ctx = agent.run(ctx)
    first_model = ctx.chosen_model

    ctx.attempts = 1
    ctx = agent.run(ctx)
    # Strong model differs from default for hi->en (claude sonnet -> gpt-4o).
    assert ctx.chosen_provider == "openai"
    assert ctx.chosen_model != first_model
