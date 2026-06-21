# Open Agency — Contributor Primer

## What this is, in one breath

Open Agency is an HR backend with exactly one verb: `request`. You hand it a
plea; it reads the written company policy and — usually — says no.

```
request(plea) -> Option[Rejection]
```

It's a real, working, policy-grounded service **and** an argument about what HR
becomes when you strip it to its function. Full detail in the [README](README.md).

## Why you can contribute here even if you don't write code

This project's whole premise is that what you can *make* matters more than the
credential next to your name. A contribution here is judged on the artifact, not
your title. If you were a project planner, a product owner, a writer, an analyst,
a QA lead — or an HR person who's seen the inside — you have a **larger** surface
here than you'd guess, because Open Agency runs on written **policy**, **test
scenarios**, **personas**, and **roadmap** as much as it runs on Python.

A merged contribution here is a real, public, linkable artifact — a thing you
point at, not a line on a résumé. That's the entire point of the project, applied
to the project itself.

## The contribution map

| You bring | You can own | Code needed? |
|---|---|---|
| Domain knowledge (HR, ops, policy) | **Policy authoring** — the HR policy docs the agent reads | No |
| Requirements / QA / test planning | **Eval scenarios** — plea + context → the decision it *should* reach | No |
| Writing / voice | **Personas** — the HR-rep characters (the sage, the hardliner, the softie) | No |
| Project planning / PM | **Roadmap & backlog** — turn the vision into scoped, claimable work | No |
| Docs / teaching | **Documentation** — guides, examples, the "how the satire works" explainer | No |
| Python | **The engine** — retrieval, tools, eval harness, conversation, UI | Yes |

Most of the highest-value work right now is in the top rows.

## If you're a project planner / product owner / non-dev — start here

Three tasks that are squarely yours and genuinely needed — each is a live issue
you can claim today:

1. **Author the eval scenario set** (#4) — the structured library of "here's a
   plea, here's the context, here's the verdict it *should* reach and the clause it
   should cite." This is requirements-and-QA work, and it's the thing that lets us
   prove the agent actually reasons correctly instead of just sounding like it
   does. Pure planning and spec.
2. **Grow the policy corpus** (#1) — right now there's one example company. Write
   more: different company archetypes, the edge-case clauses, the
   contradictory-policy traps real HR runs on. Pure domain content.
3. **Own the backlog** (#10) — groom it, scope it, write acceptance criteria,
   define milestones. If running a backlog is your craft, the backlog itself is
   yours to run.

Pick the one that sounds like you. Scope it however large or small you want — a
single policy doc is a real contribution; so is owning the whole roadmap.

## How to start (the whole process)

1. Read the [README](README.md) so you know what the thing does.
2. Browse the open **[Issues](https://github.com/BillBerger-KSO/open-agency/issues)** —
   the live, claimable backlog. New here? The
   **[`non-dev` filter](https://github.com/BillBerger-KSO/open-agency/issues?q=is%3Aissue+is%3Aopen+label%3Anon-dev)**
   shows everything that needs no code. ([BACKLOG.md](BACKLOG.md) is the same list
   as a readable overview.)
3. Claim one by **commenting on it**, so two people don't build the same thing.
4. Do the work in a branch or fork. For the non-code paths (policy, scenarios,
   personas, docs) it's just markdown — **no dev setup, no Python, no environment.**
5. Open a pull request. Rough is fine; we'll talk it through.

A policy doc or a scenario file is a text file. If you can write a clear document,
you can contribute today.

## A few norms

- **License: AGPL-3.0.** Your contribution stays free and open under the same
  terms. Nobody encloses it and sells it back. That's intentional.
- **AI is welcome — just label it.** This project is built with Claude, openly.
  Use AI to help you contribute if you like; if AI wrote prose or code in your
  contribution, say so in the PR. Honesty about which part is which is a feature
  here, not an apology.
- **The satire stays sincere.** The deadpan is the joke — an HR rep that means
  every word. Don't wink, don't break character, don't explain the bit.
- **The one hard line (from the README):** this is a thing that *reads a rulebook
  and talks.* It is never to be wired up to adjudicate a real person's real
  request. Build that and you've built the machine this project exists to make
  fun of.

Welcome. Bring the artifact.

---

*This primer's prose was written by Claude (Anthropic) on the direction of Bill
Berger. The ideas and the project are Bill's.*
