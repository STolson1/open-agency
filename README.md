# Open Agency

An HR backend with exactly one verb: **`request`**.

You send it a plea. It consults the written company policy, and — usually —
says no. That shape is the whole point:

```
request(plea) -> Option[Rejection]
```

A working policy-grounded HR endpoint, and an argument about what HR is when you
strip it to its function.

## What this is — and what it is not

It **is** a real, useful service: a question-and-answer / triage layer over your
written HR policy. Ask it something, and it answers in an HR voice, grounded in
and limited by the clauses it can actually cite.

It is **not** an automated decision-maker to point at real employees. It reads a
rulebook and talks; it does not adjudicate anyone's real request, and it should
never be wired to. Treat its output as "here is what the written policy says,"
not "here is what happens to this person." Build the second thing and you've
built the machine this project is making fun of.

## How it works

`POST /request` runs a short tool-use loop with a Claude model playing a
by-the-book HR representative:

1. The representative searches your policy (`search_policy`) for relevant clauses.
2. It commits to a structured verdict (`submit_decision`): `approved`,
   `denied`, or `needs_more_info`, with the policy clauses it relied on.

```
POST /request
  { "plea": "Can I go fully remote?", "context": { "tenure_months": 14 } }

  -> { "decision": "denied",
       "message": "Fully remote arrangements are not offered...",
       "policy_basis": ["Remote Work: fully remote arrangements are not offered"] }
```

## Quickstart

```bash
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"

cp .env.example .env        # add your ANTHROPIC_API_KEY (or use `ant auth login`)
uvicorn open_agency.main:app --reload

curl -s localhost:8000/request \
  -H 'content-type: application/json' \
  -d '{"plea":"Can I expense a standing desk for my home office?"}' | jq
```

Run the offline test suite (no key needed): `pytest`.

## Configuration

Everything is overridable without touching code. Defaults live in code;
`config.yaml` overrides them; environment variables (`OPEN_AGENCY_*`) override
the YAML. No config service, no Vault — edit a file or set an env var.

| Setting | Default | What it does |
|---|---|---|
| `model` | `claude-sonnet-4-6` | Any current Claude model id. |
| `effort` | `medium` | `low … max`. Auto-clamped to what the model supports. |
| `persona` | built-in HR voice | The representative's character. A sage, a hardliner, a softie — your call. |
| `company_name` | `Example Corp` | Named in the system prompt. |
| `policy_path` | bundled sample | Path to **your** markdown policy. |
| `max_policy_chunks` | `5` | How many policy sections a search returns. |

`model` and `effort` are independently safe to set: a combination the model
can't honor (effort on Haiku, `xhigh` on Sonnet) is degraded automatically
rather than erroring. Want a different brain? Change one line; don't fork.

Drop in your own policy by pointing `policy_path` at a markdown file. Retrieval
is plain keyword search over the file's sections — no embedding service to run.
The whole retrieval layer is one function (`policy.search`), so swapping in a
vector store later is a drop-in change.

## License

AGPL-3.0-or-later. Free to use, study, modify, and share — but if you run a
modified version as a service, you have to release your source under the same
terms. You can't enclose it and sell it back. That is intentional.

## Authorship

The code in this repository was written by Claude (Anthropic) on the direction
of Bill Berger, who set the design, made the calls, and owns the project. The
prose of this README is Claude's; the ideas and the decisions are Bill's.
