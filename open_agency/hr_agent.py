"""The HR agent — the one verb, ``request``.

A short Claude tool-use loop: the HR persona may consult the written policy
(``search_policy``) as many times as it needs, then must commit to a structured
verdict (``submit_decision``). The strict ``submit_decision`` schema is what
makes the endpoint's response a validated `Decision`.
"""

from __future__ import annotations

import json

import anthropic

from . import capabilities, policy
from .config import Settings
from .models import Decision, DecisionType

SEARCH_TOOL = {
    "name": "search_policy",
    "description": (
        "Search the written company HR policy for clauses relevant to a query. "
        "Returns matching policy sections. Call this before deciding — you may "
        "only act on what the policy actually says."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {"type": "string", "description": "What to look up in the policy."}
        },
        "required": ["query"],
        "additionalProperties": False,
    },
}

SUBMIT_TOOL = {
    "name": "submit_decision",
    "description": (
        "Submit your final decision. Call this exactly once, after you have "
        "consulted the policy and are ready to answer the employee."
    ),
    "strict": True,
    "input_schema": {
        "type": "object",
        "properties": {
            "decision": {
                "type": "string",
                "enum": ["approved", "denied", "needs_more_info"],
            },
            "message": {
                "type": "string",
                "description": "Your reply to the employee, in an HR voice.",
            },
            "policy_basis": {
                "type": "array",
                "items": {"type": "string"},
                "description": "The specific policy clauses your decision rests on.",
            },
        },
        "required": ["decision", "message", "policy_basis"],
        "additionalProperties": False,
    },
}

_MAX_TURNS = 8


class HRAgent:
    def __init__(self, settings: Settings, client: anthropic.Anthropic | None = None) -> None:
        self.s = settings
        self._client = client
        self.chunks = policy.load_chunks(settings.policy_path)

    @property
    def client(self) -> anthropic.Anthropic:
        # Lazy: the app can boot (and tests can run with an injected client)
        # without ANTHROPIC_API_KEY in the environment.
        if self._client is None:
            self._client = anthropic.Anthropic()
        return self._client

    def _system(self) -> str:
        return (
            f"{self.s.persona}\n\n"
            f"You represent {self.s.company_name}. You may only grant, deny, or "
            "defer a request based on what the written policy says. Use the "
            "search_policy tool to find the relevant clauses before deciding. If "
            "the policy does not clearly permit something, you do not have the "
            "authority to approve it — deny it or ask for the information policy "
            "would require. When you are ready, call submit_decision exactly once "
            "and cite the specific clauses you relied on."
        )

    def decide(self, plea: str, context: dict | None = None) -> Decision:
        params = capabilities.build_params(self.s.model, self.s.effort)
        user = plea if not context else f"{plea}\n\nContext: {json.dumps(context)}"
        messages: list[dict] = [{"role": "user", "content": user}]

        for _ in range(_MAX_TURNS):
            resp = self.client.messages.create(
                model=self.s.model,
                max_tokens=self.s.max_tokens,
                system=self._system(),
                tools=[SEARCH_TOOL, SUBMIT_TOOL],
                messages=messages,
                **params,
            )
            tool_uses = [b for b in resp.content if getattr(b, "type", None) == "tool_use"]

            submit = next((b for b in tool_uses if b.name == "submit_decision"), None)
            if submit is not None:
                return Decision(**submit.input)

            if tool_uses:
                messages.append({"role": "assistant", "content": resp.content})
                results = []
                for tu in tool_uses:
                    if tu.name == "search_policy":
                        hits = policy.search(
                            self.chunks, tu.input.get("query", ""), self.s.max_policy_chunks
                        )
                        out = "\n\n".join(f"## {h}\n{b}" for h, b in hits) or "No matching policy found."
                        results.append({"type": "tool_result", "tool_use_id": tu.id, "content": out})
                    else:
                        results.append(
                            {
                                "type": "tool_result",
                                "tool_use_id": tu.id,
                                "content": "Unknown tool.",
                                "is_error": True,
                            }
                        )
                messages.append({"role": "user", "content": results})
                continue

            # Model stopped without deciding — nudge it once toward submit_decision.
            messages.append({"role": "assistant", "content": resp.content})
            messages.append(
                {
                    "role": "user",
                    "content": "Call submit_decision now with your final decision.",
                }
            )

        # Loop exhausted without a decision: defer rather than fabricate one.
        return Decision(
            decision=DecisionType.needs_more_info,
            message="I could not resolve this request against the policy. Please add detail and resubmit.",
            policy_basis=[],
        )
