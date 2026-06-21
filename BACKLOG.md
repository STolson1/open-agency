# Open Agency — Suggested Backlog

> **These items are live as [GitHub Issues](https://github.com/BillBerger-KSO/open-agency/issues) — claim one by commenting there.** This file is the readable overview; the Issues are the claimable list.

A starter list of takeable work. New to the project? Read the
[PRIMER](PRIMER.md) first.

**Tags:** **[non-dev]** needs no code · **[good-first]** small and self-contained ·
**[dev]** Python · **[stretch]** bigger / open-ended.

Pick anything. Scope it to taste — a single doc is a real contribution. Claim it
by opening or commenting on an issue so two people don't build the same thing.

---

## Policy corpus — content, no code

- **[non-dev] [good-first] Add a company policy.** Write a realistic HR policy
  (markdown) for a fictional company archetype — a scrappy startup, a bloated
  enterprise, a union shop, an agency. Model it on
  `open_agency/policies/example_company.md`.
  *Done when:* a new `policies/<name>.md` covers the common request areas (PTO,
  remote work, expenses, conduct, leave) with clear, citable clauses.

- **[non-dev] Edge-case clause pack.** Add the policy traps real HR runs on:
  contradictory clauses, "subject to manager discretion," eligibility gated by
  tenure, the silent-no that isn't written anywhere.
  *Done when:* a policy doc (or section) that makes the agent's job genuinely hard.

- **[non-dev] Policy authoring guide.** Document how to write a policy the agent
  reads *well* — sectioning, clause phrasing, what the retrieval keys on.
  *Done when:* a short `docs/writing-policies.md`.

## Eval scenarios — requirements / QA, no code

- **[non-dev] [good-first] Seed the eval set.** Author a structured catalog of
  test cases. Each case is a `plea`, optional `context`, the expected `decision`
  (`approved` / `denied` / `needs_more_info`), and the policy clause it should
  cite.
  *Done when:* an `evals/` file with ~15–20 cases against the example policy.

- **[non-dev] Adversarial pleas.** Write the hard cases: pleas that try to argue
  the agent into a yes it shouldn't give; ambiguous requests; missing-context
  cases that *should* come back `needs_more_info`.
  *Done when:* a scenario set aimed squarely at reasoning failures.

- **[non-dev] Decision rubric.** Define what "correct" means for a verdict — right
  decision? right clause cited? right tone? — so evals can be scored the same way
  every time.
  *Done when:* a short rubric a future harness can implement.

## Personas — writing, no code

- **[non-dev] [good-first] Persona library.** Write 3–5 HR-rep personas as config
  plus character notes: the by-the-book sage, the hardliner, the softie who still
  says no, the corporate-cheerful. The deadpan stays sincere.
  *Done when:* persona definitions that drop into the `persona` config knob.

## Docs & onboarding — writing, no code

- **[non-dev] Usage examples.** A page of real `POST /request` examples — the
  plea, the context, the response.
  *Done when:* `docs/examples.md`.

- **[non-dev] "How the satire works."** A short explainer of the project's
  argument, for newcomers who read it as just a tool and miss the knife.
  *Done when:* a docs page.

## Project management — planning, no code

- **[non-dev] Own the backlog.** Take this file over: groom it, convert items to
  GitHub issues, add acceptance criteria, define milestones.
  *Done when:* a living, triaged backlog you steward.

- **[non-dev] Write the roadmap.** Turn the vision into phases (v0.1 → v1.0):
  what's the minimum lovable HR rep, what's the demo, what's the eval-proven
  release.
  *Done when:* a `ROADMAP.md`.

## Engine — Python

- **[dev] [good-first] Eval harness.** A runner that executes the eval scenarios
  against `/request` and scores them against the rubric. Pairs directly with the
  non-dev-authored scenario set — content plus code equals a real test suite.
  *Done when:* `python -m evals` runs the catalog and reports pass/fail.

- **[dev] Retrieval upgrade.** Swap the keyword `policy.search` for embeddings / a
  vector store. It's one function by design.
  *Done when:* retrieval is pluggable and an embedding path works.

- **[dev] Multi-turn pleas.** Handle `needs_more_info` as an actual follow-up
  conversation instead of a dead end.
  *Done when:* a plea can be resolved across turns.

- **[dev] [stretch] Web demo.** A minimal front-end: type a plea, watch the
  by-the-book rep search policy and rule on you.
  *Done when:* a local demo page hits the API.

- **[dev] Observability.** Log every decision with the clauses it cited, so policy
  gaps become visible.
  *Done when:* structured decision logs.

---

## The collaboration that makes the point

Notice the seam: a **planner** authors the eval scenarios (content) and a **dev**
builds the eval harness (code), and together they're a real test suite neither
could ship alone. Same with policy authors feeding the engine. That's the
all-roles thesis working in practice — pick your half, and someone else picks the
other.

---

*This backlog's prose was written by Claude (Anthropic) on the direction of Bill
Berger. The ideas and the project are Bill's.*
