from __future__ import annotations

import logging
from collections.abc import Callable, Sequence

from framework.agent import BaseAgent
from framework.context import Context

log = logging.getLogger(__name__)


class PipelineError(RuntimeError):
    pass


StopFn = Callable[[Context], bool]


class Pipeline:
    def __init__(
        self,
        agents: Sequence[BaseAgent],
        *,
        stop_when: StopFn | None = None,
        short_circuit_on_error: bool = True,
    ) -> None:
        self.agents = list(agents)
        self.stop_when = stop_when
        self.short_circuit_on_error = short_circuit_on_error

    def run(self, ctx: Context) -> Context:
        for agent in self.agents:
            ctx = agent(ctx)
            if self.short_circuit_on_error and ctx.errors:
                log.warning("pipeline short-circuit at %s: %s", agent.name, ctx.errors[-1])
                break
            if self.stop_when and self.stop_when(ctx):
                log.info("pipeline stop_when satisfied at %s", agent.name)
                break
        return ctx
