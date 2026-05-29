from __future__ import annotations

import logging
import time
from abc import ABC, abstractmethod

from framework.context import Context

log = logging.getLogger(__name__)


class BaseAgent(ABC):
    name: str = "agent"

    @abstractmethod
    def run(self, ctx: Context) -> Context: ...

    def __call__(self, ctx: Context) -> Context:
        start = time.perf_counter()
        try:
            ctx = self.run(ctx)
        except Exception as exc:
            ctx.fail(f"{self.name}: {exc}")
            log.exception("agent %s raised", self.name)
        finally:
            ctx.latency_ms[self.name] = (time.perf_counter() - start) * 1000
        return ctx
