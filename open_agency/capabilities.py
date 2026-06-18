"""Capability-aware request parameters.

The `model` and `effort` settings are independently configurable, but they are
NOT independently free: Haiku rejects the effort parameter entirely and has no
adaptive thinking; `xhigh`/`max` exist only on Opus-tier / Fable. This module
builds the per-request kwargs so a deployer can dial any model/effort
combination via config without forking AND without ever triggering a 400 — an
unsupported effort is clamped down, unsupported thinking is dropped.

The static maps below reflect the model lineup as of this writing. For a
self-updating alternative, replace `build_params` with a startup probe of the
Models API (`client.models.retrieve(model).capabilities`).
"""

from __future__ import annotations

_EFFORT_ORDER = ["low", "medium", "high", "xhigh", "max"]

# Per-model allowed effort levels. A model absent from this map gets the
# conservative default set; a model mapped to an empty set takes no effort param.
_EFFORT_SUPPORT: dict[str, set[str]] = {
    "claude-haiku-4-5": set(),  # rejects effort entirely
    "claude-sonnet-4-5": set(),  # rejects effort entirely
    "claude-sonnet-4-6": {"low", "medium", "high", "max"},  # no xhigh
    "claude-opus-4-6": {"low", "medium", "high", "max"},  # no xhigh
    "claude-opus-4-7": {"low", "medium", "high", "xhigh", "max"},
    "claude-opus-4-8": {"low", "medium", "high", "xhigh", "max"},
    "claude-fable-5": {"low", "medium", "high", "xhigh", "max"},
}
# Unknown / future models: assume effort works but stay below the tier-specific
# top levels that commonly 400.
_DEFAULT_EFFORT_SUPPORT = {"low", "medium", "high"}

# Models that do NOT support adaptive thinking.
_NO_ADAPTIVE_THINKING = {"claude-haiku-4-5", "claude-sonnet-4-5"}


def effort_for(model: str, requested: str) -> str | None:
    """Return the effort level to send, clamped to what the model accepts.

    Returns ``None`` if the model takes no effort parameter at all.
    """
    allowed = _EFFORT_SUPPORT.get(model, _DEFAULT_EFFORT_SUPPORT)
    if not allowed:
        return None
    if requested in allowed:
        return requested
    # clamp down to the highest allowed level at or below the request
    idx = _EFFORT_ORDER.index(requested) if requested in _EFFORT_ORDER else len(_EFFORT_ORDER) - 1
    for level in reversed(_EFFORT_ORDER[: idx + 1]):
        if level in allowed:
            return level
    return None


def thinking_for(model: str) -> dict | None:
    """Return the thinking config to send, or ``None`` if unsupported."""
    if model in _NO_ADAPTIVE_THINKING:
        return None
    return {"type": "adaptive"}


def build_params(model: str, effort: str) -> dict:
    """Build the thinking/effort kwargs for ``messages.create`` for this model."""
    params: dict = {}
    thinking = thinking_for(model)
    if thinking is not None:
        params["thinking"] = thinking
    eff = effort_for(model, effort)
    if eff is not None:
        params["output_config"] = {"effort": eff}
    return params
