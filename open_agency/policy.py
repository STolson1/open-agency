"""The policy — the searchable rulebook.

Each deployer points ``policy_path`` at their own markdown policy. It is split
into sections on markdown headings; ``search`` does plain keyword scoring over
those sections. That's deliberately simple: no vector DB, no embedding service
to run. The whole retrieval layer sits behind one function, so swapping in a
vector store later is a drop-in change that doesn't touch the agent.
"""

from __future__ import annotations

import re
from pathlib import Path

_WORD = re.compile(r"\w+")

# (heading, body) section pair
Chunk = tuple[str, str]


def load_chunks(path: str | Path) -> list[Chunk]:
    """Split a markdown policy file into (heading, body) sections."""
    text = Path(path).read_text(encoding="utf-8")
    chunks: list[Chunk] = []
    heading = "Policy"
    lines: list[str] = []
    for line in text.splitlines():
        if line.lstrip().startswith("#"):
            if any(s.strip() for s in lines):
                chunks.append((heading, "\n".join(lines).strip()))
            heading = line.lstrip("#").strip() or "Policy"
            lines = [line]
        else:
            lines.append(line)
    if any(s.strip() for s in lines):
        chunks.append((heading, "\n".join(lines).strip()))
    return chunks


def search(chunks: list[Chunk], query: str, k: int) -> list[Chunk]:
    """Return up to ``k`` policy sections most relevant to ``query``.

    Keyword-overlap scoring. If nothing matches, returns the first section so the
    agent always sees *some* policy rather than an empty result.
    """
    q = set(w.lower() for w in _WORD.findall(query))
    scored: list[tuple[int, Chunk]] = []
    for heading, body in chunks:
        words = set(w.lower() for w in _WORD.findall(f"{heading} {body}"))
        score = len(q & words)
        if score:
            scored.append((score, (heading, body)))
    scored.sort(key=lambda s: s[0], reverse=True)
    hits = [c for _, c in scored[:k]]
    if not hits and chunks:
        hits = chunks[:1]
    return hits
