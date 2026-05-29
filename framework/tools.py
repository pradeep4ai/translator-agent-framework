from __future__ import annotations

import inspect
from collections.abc import Callable
from dataclasses import dataclass
from typing import Any


@dataclass
class Tool:
    name: str
    fn: Callable[..., Any]
    description: str
    signature: inspect.Signature


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, Tool] = {}

    def register(self, fn: Callable[..., Any], name: str | None = None) -> Tool:
        tool_name = name or fn.__name__
        if tool_name in self._tools:
            raise ValueError(f"Tool already registered: {tool_name}")
        t = Tool(
            name=tool_name,
            fn=fn,
            description=(fn.__doc__ or "").strip(),
            signature=inspect.signature(fn),
        )
        self._tools[tool_name] = t
        return t

    def get(self, name: str) -> Tool:
        return self._tools[name]

    def call(self, name: str, *args: Any, **kwargs: Any) -> Any:
        return self._tools[name].fn(*args, **kwargs)

    def list(self) -> list[Tool]:
        return list(self._tools.values())


_GLOBAL = ToolRegistry()


def tool(fn: Callable[..., Any] | None = None, *, name: str | None = None):
    """Decorator to register a function as a tool in the global registry."""
    def wrap(f: Callable[..., Any]) -> Callable[..., Any]:
        _GLOBAL.register(f, name=name)
        return f
    return wrap(fn) if fn is not None else wrap


def global_registry() -> ToolRegistry:
    return _GLOBAL
