"""Offline tests — no API key, no network. The Anthropic client is faked."""

from __future__ import annotations

from types import SimpleNamespace

from fastapi.testclient import TestClient

from open_agency import capabilities, main, policy
from open_agency.config import Settings
from open_agency.hr_agent import HRAgent
from open_agency.models import Decision


# --- capability degradation ---

def test_effort_clamps_per_model():
    assert capabilities.effort_for("claude-sonnet-4-6", "xhigh") == "high"  # sonnet has no xhigh
    assert capabilities.effort_for("claude-opus-4-8", "xhigh") == "xhigh"
    assert capabilities.effort_for("claude-haiku-4-5", "high") is None  # haiku takes no effort
    assert capabilities.effort_for("some-future-model", "max") == "high"  # unknown -> conservative


def test_thinking_dropped_for_unsupported():
    assert capabilities.thinking_for("claude-haiku-4-5") is None
    assert capabilities.thinking_for("claude-sonnet-4-6") == {"type": "adaptive"}


def test_build_params_haiku_is_bare():
    # Haiku would 400 on either param; build_params must send neither.
    assert capabilities.build_params("claude-haiku-4-5", "high") == {}


# --- policy search ---

def test_policy_search_finds_relevant_section():
    chunks = policy.load_chunks(Settings().policy_path)
    hits = policy.search(chunks, "can I work remotely full time", k=3)
    assert any("Remote Work" in h for h, _ in hits)


# --- the agent loop, with a faked client ---

class _FakeMessages:
    """Returns a search_policy call first, then a submit_decision call."""

    def __init__(self) -> None:
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        if self.calls == 1:
            block = SimpleNamespace(
                type="tool_use", name="search_policy", id="t1", input={"query": "remote work"}
            )
            return SimpleNamespace(content=[block], stop_reason="tool_use")
        block = SimpleNamespace(
            type="tool_use",
            name="submit_decision",
            id="t2",
            input={
                "decision": "denied",
                "message": "Fully remote arrangements are not offered.",
                "policy_basis": ["Remote Work: fully remote arrangements are not offered"],
            },
        )
        return SimpleNamespace(content=[block], stop_reason="tool_use")


class _FakeClient:
    def __init__(self) -> None:
        self.messages = _FakeMessages()


def test_agent_searches_then_decides():
    agent = HRAgent(Settings(), client=_FakeClient())
    decision = agent.decide("Can I go fully remote?")
    assert isinstance(decision, Decision)
    assert decision.decision.value == "denied"
    assert decision.policy_basis


def test_request_endpoint():
    # Swap the app's agent for one backed by the fake client.
    main.agent = HRAgent(Settings(), client=_FakeClient())
    client = TestClient(main.app)

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["model"]

    resp = client.post("/request", json={"plea": "Can I go fully remote?"})
    assert resp.status_code == 200
    body = resp.json()
    assert body["decision"] == "denied"
    assert body["message"]
